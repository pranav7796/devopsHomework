"""Capture a dedicated opaque Foot terminal with Grim; never provision AWS.

AWS views show explicitly dated saved logs, not current running resources.
Run from the repository root. Requires the owner's Wayland desktop session.
"""
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent
SOURCES = set()


def read(path):
    SOURCES.add(path)
    return (ROOT / path).read_text()


def load(path):
    return json.loads(read(path))


def show(view):
    print("devopsHomework | submission evidence | 21 October 2026 (IST)")
    print("Actual terminal capture. AWS panels display SAVED 20 October UTC execution logs.")
    print("The temporary AWS resources were subsequently destroyed; this does not rerun them.\n")
    if view == "plan":
        path = "evidence/aws-plans/s19-plan.txt"
        text = read(path)
        print("SESSION 19: authenticated Terraform plan (resource/summary excerpts)")
        print("Source:", path)
        print("SHA256:", hashlib.sha256(text.encode()).hexdigest(), "\n")
        for line in text.splitlines():
            if re.match(r"  # aws_|Plan:|  \+ (bucket_name|instance_public_ip|vpc_id)", line):
                print(line)
        print("\nFull original plan, command exit codes and input/source hashes remain in evidence/aws-plans/.")
    elif view in ("s18", "s19", "final"):
        prefix = "evidence/aws-execution/" + view
        summary = next(p for p in load("evidence/aws-execution/summary.json")["projects"] if p["exercise"] == view)
        print("AWS LIFECYCLE:", summary["project"])
        print("Original execution:", summary["started_at_utc"], "to", summary["finished_at_utc"])
        print("Source prefix:", prefix, "\n")
        for phase in ("apply", "destroy"):
            lines = read(prefix + "-" + phase + ".txt").splitlines()
            print(phase + ".txt:", next(line for line in lines if "Apply complete!" in line))
        print("\nS3 bucket:", summary["bucket"])
        public = load(prefix + "-bucket-public-access.txt")["PublicAccessBlockConfiguration"]
        print("bucket-public-access.txt:", ", ".join(k + "=" + str(v) for k, v in public.items()))
        print("bucket-versioning.txt:", load(prefix + "-bucket-versioning.txt"))
        encryption = load(prefix + "-bucket-encryption.txt")
        print("bucket-encryption.txt: SSEAlgorithm =", encryption["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]["SSEAlgorithm"])
        if view != "s18":
            print("\nhttp-attempts.json:", json.dumps(load(prefix + "-http-attempts.json")))
            print("http.txt:", read(prefix + "-http.txt").strip())
            instance = load(prefix + "-instance-after-cleanup.txt")["Reservations"][0]["Instances"][0]
            print("instance-after-cleanup.txt:", instance["InstanceId"], instance["State"])
            for kind in ("vpc", "volume"):
                extra = "-" + summary["volume_ids"][0] if kind == "volume" else ""
                error = read(prefix + "-" + kind + "-after-cleanup" + extra + "-stderr.txt").strip()
                print(kind + "-after-cleanup: " + error.split("when calling")[0].strip())
        print("bucket-after-cleanup-stderr.txt:", read(prefix + "-bucket-after-cleanup-stderr.txt").strip())
        state = read(prefix + "-state-after-cleanup.txt").strip()
        print("state-after-cleanup.txt:", repr(state), "(empty Terraform state)")
        print("\nExact AWS commands, timestamps and exit codes: evidence/aws-execution/command-results.json")
    elif view == "ci":
        data = load("evidence/screenshots-2026-10-21/ci-run.json")
        print("GITHUB ACTIONS | fresh gh run view API response (saved alongside this capture)")
        print(data["url"])
        print("Run:", data["databaseId"], "|", data["status"], "|", data["conclusion"])
        print("Source commit:", data["headSha"], "\n")
        for job in data["jobs"]:
            print(job["name"], "|", job["conclusion"], "| completed", job["completedAt"])
            for step in job["steps"]:
                if not step["name"].startswith(("Post ", "Set up", "Complete ", "Run actions/", "Run docker/login")):
                    print("  " + step["name"] + ": " + step["conclusion"])
    else:
        raise ValueError(view)
    print("\nCaptured at:", datetime.datetime.now(datetime.timezone.utc).isoformat())


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--show":
        show(sys.argv[2])
        sys.exit(0)
    if sys.argv[1:] != ["--capture"]:
        raise SystemExit("Usage: python capture.py --capture | --show {plan,s18,s19,final,ci}")
    gh = "/home/pranav/.local/share/mise/installs/gh/latest/gh_2.102.0_linux_amd64/bin/gh"
    command = [gh, "run", "view", "39501169416", "--repo", "pranav7796/devopsHomework", "--json", "databaseId,headSha,status,conclusion,url,jobs"]
    (OUT / "ci-run.json").write_text(subprocess.check_output(command, text=True))
    subprocess.run(["foot", "-c", "/dev/null", "-o", "colors-dark.alpha=1.0", "-C"], check=True)
    records = []
    for view in ("plan", "s18", "s19", "final", "ci"):
        image = ROOT / "terraform-cloud/evidence/terraform-plan.png" if view == "plan" else OUT / (view + "-evidence.png")
        image.parent.mkdir(parents=True, exist_ok=True)
        app_id = "homework-evidence-capture"
        cmd = ["foot", "-c", "/dev/null", "-F", "-H", "-a", app_id, "-T", "Homework evidence", "-f", "monospace:size=11", "-o", "colors-dark.alpha=1.0", sys.executable, str(pathlib.Path(__file__).resolve()), "--show", view]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        try:
            client = None
            for _ in range(40):
                clients = json.loads(subprocess.check_output(["hyprctl", "-j", "clients"], text=True))
                client = next((c for c in clients if c["class"] == app_id and c["pid"] == process.pid), None)
                if client and client["size"] == [1366, 768]:
                    break
                time.sleep(0.1)
            if not client or process.poll() is not None:
                raise RuntimeError("Dedicated terminal did not open: " + process.stderr.read().decode())
            time.sleep(1)
            geometry = f'{client["at"][0]},{client["at"][1]} {client["size"][0]}x{client["size"][1]}'
            subprocess.run(["grim", "-g", geometry, str(image)], check=True)
            # Re-read exactly the sources displayed to record their content hashes.
            SOURCES.clear()
            show(view)
            records.append({"view": view, "image": str(image.relative_to(ROOT)), "captured_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "terminal_command": cmd, "capture_command": ["grim", "-g", geometry, str(image)], "sha256": hashlib.sha256(image.read_bytes()).hexdigest(), "sources": [{"path": p, "sha256": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()} for p in sorted(SOURCES)]})
        finally:
            process.terminate()
            process.wait(timeout=5)
    (OUT / "provenance.json").write_text(json.dumps({"ci_query_command": command, "capture_method": "Actual dedicated Foot terminal window captured by Grim on the owner's Wayland desktop; no image synthesis or editing", "records": records}, indent=2) + "\n")
