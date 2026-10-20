# Authenticated homework AWS plans

Prepared on 21 October 2026 (IST), profile `devops-new`, account `525426877661`, Sydney `ap-southeast-2`.

- [Command exit codes and UTC timestamps](command-results.json).
- [Exact resources, trusted CIDR, image, plan/source hashes](summary.json).
- [Session 18: 4 additions](s18-plan.txt), [Session 19: 11 additions](s19-plan.txt), [final project: 11 additions](final-plan.txt).
- Each project's `*-init.txt`, `*-fmt.txt`, `*-validate.txt` records its own executed checks. `identity.txt` and `image.txt` are real AWS JSON responses saved as text.
- [Official Price List responses summarized](price-summary.json), [AMI disk details](ami-details.json). Full service responses are retained as `price-ec2.json`, `price-storage.json` and `price-ipv4.json`.

**At plan capture these plans were unapplied.** They were subsequently applied, independently verified, and destroyed. [Actual lifecycle and cleanup/absence proof](../aws-execution/README.md). The `applied: false` field in the dated planning summary describes the preparation snapshot; it is not current execution status. New PNG capture remains unavailable. Original saved-plan JSON was inspected in memory; binaries, state and private input snapshots are not public artifacts. No credentials are contained in the public outputs.

The read-only planning helper is `python3 scripts/prepare-aws-plans.py` from the repository root. The [reviewed workflow and approval scope](../../AWS-HOMEWORK.md) explain the distinct projects, costs and cleanup order. Existing RelayDesk resources are outside this scope.
