"""Run the four Session 10 strategies in a disposable local Minikube namespace."""
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence/completion-2026-10-21"
NS = "homework-strategy-check"
BASE = ["kubectl", "--context", "minikube", "--request-timeout=15s", "-n", NS]
SOURCE = ROOT / "09-kubernetes-pods-deployments"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    records, results = [], {}

    def run(*args, data=None, timeout=90):
        command = [*BASE, *args]
        started = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, cwd=ROOT, input=data, capture_output=True, text=True, timeout=timeout)
        records.append({"command": command, "started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(), "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        (OUT / "strategy-commands.json").write_text(json.dumps(records, indent=2) + "\n")
        if result.returncode:
            raise RuntimeError(result.stderr or result.stdout)
        return result.stdout

    def apply(folder, filename):
        path = SOURCE / folder / filename
        if filename.startswith("service"):
            # Preserve selector/routing; avoid cluster-wide NodePort conflicts.
            # Adaptation is recorded explicitly and does not edit the source file.
            manifest = path.read_text().replace("type: NodePort", "type: ClusterIP")
            manifest = re.sub(r"^\s+nodePort:.*\n", "", manifest, flags=re.MULTILINE)
            run("apply", "-f", "-", data=manifest)
        else:
            run("apply", "-f", str(path))

    def ready(name):
        run("rollout", "status", "deployment/" + name, "--timeout=150s", timeout=180)

    def http(deployment, service, marker):
        for _ in range(12):
            body = run("exec", "deploy/" + deployment, "--", "wget", "-q", "-O", "-", "http://" + service)
            if marker in body:
                return body
            time.sleep(1)
        raise AssertionError("Expected response missing: " + marker)

    def endpoints(service, counts):
        for _ in range(30):
            slices = json.loads(run("get", "endpointslices", "-l", "kubernetes.io/service-name=" + service, "-o", "json"))
            names = [e["targetRef"]["name"] for item in slices["items"] for e in item.get("endpoints", []) if e.get("conditions", {}).get("ready")]
            actual = {prefix: sum(n.startswith(prefix + "-") for n in names) for prefix in counts}
            if actual == counts and len(names) == sum(counts.values()):
                return actual
            time.sleep(1)
        raise AssertionError(f"Endpoint counts differ: {actual} != {counts}")

    # Fail closed unless this is the named local node, never the active EKS context.
    nodes = json.loads(run("get", "nodes", "-o", "json"))["items"]
    if len(nodes) != 1 or nodes[0]["metadata"]["name"] != "minikube":
        raise RuntimeError("Expected the existing local minikube profile; no resources were changed.")
    namespace = json.loads(run("create", "namespace", NS, "-o", "json"))
    namespace_uid = namespace["metadata"]["uid"]
    try:
        folder = "01-rolling-update"
        apply(folder, "deployment-v1.yaml"); apply(folder, "service.yaml"); ready("app-rolling")
        http("app-rolling", "app-rolling-service", "VERSION: v1")
        apply(folder, "deployment-v2.yaml"); ready("app-rolling")
        http("app-rolling", "app-rolling-service", "VERSION: v2")
        deployment = json.loads(run("get", "deploy", "app-rolling", "-o", "json"))
        assert deployment["status"]["availableReplicas"] == 4
        results["rolling"] = {"status": "PASS", "ready_replicas": 4, "strategy": deployment["spec"]["strategy"], "limits": "Versions and readiness verified; continuous zero-downtime HTTP availability was not measured."}
        run("delete", "deploy/app-rolling", "svc/app-rolling-service", "--wait=true")

        folder = "02-blue-green"
        apply(folder, "deployment-blue.yaml"); apply(folder, "deployment-green.yaml")
        ready("app-blue"); ready("app-green")
        apply(folder, "service-blue.yaml"); endpoints("myapp-service", {"app-blue": 3})
        http("app-blue", "myapp-service", "BLUE ENVIRONMENT")
        apply(folder, "service-green.yaml"); endpoints("myapp-service", {"app-green": 3})
        http("app-green", "myapp-service", "GREEN ENVIRONMENT")
        apply(folder, "service-blue.yaml"); endpoints("myapp-service", {"app-blue": 3})
        http("app-blue", "myapp-service", "BLUE ENVIRONMENT")
        results["blue_green"] = {"status": "PASS", "ready_replicas_per_version": 3, "routing": "blue -> green -> blue verified with Ready endpoints and HTTP"}
        run("delete", "deploy/app-blue", "deploy/app-green", "svc/myapp-service", "--wait=true")

        folder = "03-canary"
        apply(folder, "deployment-stable.yaml"); apply(folder, "deployment-canary.yaml"); apply(folder, "service.yaml")
        ready("app-stable"); ready("app-canary")
        counts = endpoints("myapp-canary-service", {"app-stable": 9, "app-canary": 1})
        command = "i=0; while [ \"$i\" -lt 100 ]; do wget -q -O - http://myapp-canary-service || exit 1; i=$((i+1)); done"
        traffic = run("exec", "deploy/app-stable", "--", "sh", "-c", command)
        observed = {"stable": traffic.count("STABLE v1"), "canary": traffic.count("CANARY v2")}
        assert sum(observed.values()) == 100 and all(observed.values())
        run("scale", "deployment/app-canary", "--replicas=0")
        endpoints("myapp-canary-service", {"app-stable": 9})
        http("app-stable", "myapp-canary-service", "STABLE v1")
        results["canary"] = {"status": "PASS", "ready_endpoints_before_rollback": counts, "observed_100_new_requests": observed, "rollback": "stable-only endpoints and response verified; endpoint ratio does not guarantee exact request percentages"}
        run("delete", "deploy/app-stable", "deploy/app-canary", "svc/myapp-canary-service", "--wait=true")

        folder = "04-recreate"
        apply(folder, "deployment-v1.yaml"); apply(folder, "service.yaml"); ready("app-recreate")
        http("app-recreate", "app-recreate-service", "VERSION: v1")
        old = json.loads(run("get", "pods", "-l", "app=app-recreate", "-o", "json"))
        old_uids = {p["metadata"]["uid"] for p in old["items"]}
        apply(folder, "deployment-v2.yaml"); ready("app-recreate")
        http("app-recreate", "app-recreate-service", "VERSION: v2")
        new = json.loads(run("get", "pods", "-l", "app=app-recreate", "-o", "json"))
        assert len(new["items"]) == 3 and not old_uids.intersection(p["metadata"]["uid"] for p in new["items"])
        results["recreate"] = {"status": "PASS", "ready_replicas": 3, "old_pods_replaced": True, "limits": "Replacement/response verified; downtime duration not measured."}
        run("get", "pods,deploy,svc", "-o", "wide")
    finally:
        current = json.loads(run("get", "namespace", NS, "-o", "json"))
        if current["metadata"]["uid"] != namespace_uid:
            raise RuntimeError("Namespace identity changed; refusing cleanup.")
        run("delete", "namespace", NS, "--wait=true", "--timeout=120s", timeout=150)
        results["scope"] = {"context": "minikube", "namespace": NS, "cleanup": "Only this newly created namespace was deleted", "service_adaptation": "NodePort -> ClusterIP and nodePort removed to avoid collisions with preexisting labs; selectors/targetPorts preserved", "verified_at_utc": datetime.now(timezone.utc).isoformat()}
        (OUT / "strategy-results.json").write_text(json.dumps(results, indent=2) + "\n")
    assert len([v for v in results.values() if v.get("status") == "PASS"]) == 4
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
