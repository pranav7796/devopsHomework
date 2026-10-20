"""Prepare real homework plans and evidence; never apply or destroy resources."""
import argparse
from datetime import datetime, timezone
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ACCOUNT, PROFILE, REGION = "525426877661", "devops-new", "ap-southeast-2"
PROJECTS = {"terraform-s3-demo": "s18", "terraform-cloud": "s19", "final-devops-project/terraform": "final"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--admin-cidr", help="Trusted public IPv4 /32; defaults to current egress via checkip.amazonaws.com")
    args = parser.parse_args()
    out = ROOT / "evidence" / "aws-plans"
    out.mkdir(parents=True, exist_ok=True)
    records = []

    def run(name, command, save=True):
        started = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=300)
        record = {"command": command, "started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(), "exit_code": result.returncode, "stderr": result.stderr}
        if save:
            filename = name + ".txt"
            (out / filename).write_text(result.stdout)
            record["stdout"] = filename
        records.append(record)
        (out / "command-results.json").write_text(json.dumps(records, indent=2) + "\n")
        if result.returncode:
            raise RuntimeError(f"{name} failed; see evidence/aws-plans/command-results.json. An expired session needs aws login --profile {PROFILE} --region {REGION}.")
        return result.stdout

    def aws(name, *command):
        return json.loads(run(name, ["aws", *command, "--profile", PROFILE, "--region", REGION, "--output", "json", "--no-cli-pager"]))

    identity = aws("identity", "sts", "get-caller-identity")
    if identity["Account"] != ACCOUNT:
        raise RuntimeError("Wrong AWS account; no Terraform command was run.")
    image = aws("image", "ssm", "get-parameter", "--name", "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64")["Parameter"]["Value"]
    cidr = args.admin_cidr
    if cidr is None:
        with urllib.request.urlopen("https://checkip.amazonaws.com", timeout=10) as response:
            cidr = response.read().decode().strip() + "/32"
    network = ipaddress.ip_network(cidr, strict=True)
    if network.version != 4 or network.prefixlen != 32 or not network.network_address.is_global:
        raise RuntimeError("admin-cidr must be one public IPv4 address with a /32 prefix.")
    summary = {"prepared_at_utc": datetime.now(timezone.utc).isoformat(), "account": ACCOUNT, "profile": PROFILE, "region": REGION, "ami_id": image, "admin_cidr": str(network), "applied": False, "projects": []}
    for project, exercise in PROJECTS.items():
        prefix = exercise + "-"
        base = ["bash", "scripts/terraform-readonly.sh", project]
        for name, command in [("init", ["init", "-input=false", "-lockfile=readonly", "-no-color"]), ("fmt", ["fmt", "-check"]), ("validate", ["validate", "-no-color"])]:
            run(prefix + name, base + command)
        bucket = f"devops-homework-24bcs10006-{exercise}-{ACCOUNT}"
        variables = {"aws_region": REGION, "bucket_name": bucket}
        if exercise != "s18":
            variables.update(ami_id=image, ssh_cidr=str(network))
        private = ROOT / "evidence/private/aws-inputs"
        private.mkdir(parents=True, exist_ok=True)
        os.chmod(ROOT / "evidence/private", 0o700)
        os.chmod(private, 0o700)
        snapshot = private / (exercise + ".tfvars.json")
        snapshot.write_text(json.dumps(variables, indent=2) + "\n")
        os.chmod(snapshot, 0o600)
        # Saved plans may contain sensitive state; private permissions plus ignore rules.
        old_umask = os.umask(0o077)
        try:
            run(prefix + "plan", base + ["plan", "-input=false", "-no-color", "-out=tfplan-completion", "-var-file=" + str(snapshot)])
        finally:
            os.umask(old_umask)
        plan = json.loads(run(prefix + "plan-json", base + ["show", "-json", "tfplan-completion"], save=False))
        assert plan["variables"]["aws_region"]["value"] == REGION
        assert plan["configuration"]["provider_config"]["aws"]["expressions"]["allowed_account_ids"]["constant_value"] == [ACCOUNT]
        changes = [{"address": item["address"], "actions": item["change"]["actions"]} for item in plan.get("resource_changes", [])]
        if any(item["actions"] not in (["create"], ["read"], ["no-op"]) for item in changes):
            raise RuntimeError("Plan includes changes/deletions to existing resources; review manually. No apply was run.")
        summary["projects"].append({"directory": project, "bucket": bucket, "input_snapshot": str(snapshot.relative_to(ROOT)), "saved_plan": project + "/tfplan-completion", "plan_sha256": hashlib.sha256((ROOT / project / "tfplan-completion").read_bytes()).hexdigest(), "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT / project).glob("*.tf"))}, "changes": changes})
        (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("Read-only plans prepared. No AWS resources were created, changed or deleted. Review before requesting deployment approval.")


if __name__ == "__main__":
    main()
