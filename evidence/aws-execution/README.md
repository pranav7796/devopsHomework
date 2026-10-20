# Actual homework AWS execution — 21 October 2026 (IST)

**All three reviewed plans were applied, independently verified and destroyed.** No homework resources remain running. Only newly created resources recorded by these separate states were deleted. Existing RelayDesk/EKS was excluded and its ARN/status/version/VPC were checked unchanged and ACTIVE before and after.

[Complete results and created IDs](summary.json), [commands/UTC timestamps/exit codes](command-results.json), [authorization/saved-plan hashes](AUTHORIZATION.md), [full execution progress](../aws-execution-run.txt).

| Project | Apply | Live verification | Cleanup | Exact evidence |
|---|---|---|---|---|
| terraform-s3-demo | PASS | PASS | PASS | [apply](s18-apply.txt), [show](s18-show.txt), [output](s18-output.txt), [destroy](s18-destroy.txt), [cleanup review](s18-cleanup-audit.json) |
| terraform-cloud | PASS | PASS | PASS | [apply](s19-apply.txt), [show](s19-show.txt), [output](s19-output.txt), [destroy](s19-destroy.txt), [cleanup review](s19-cleanup-audit.json) |
| final-devops-project/terraform | PASS | PASS | PASS | [apply](final-apply.txt), [show](final-show.txt), [output](final-output.txt), [destroy](final-destroy.txt), [cleanup review](final-cleanup-audit.json) |

For every bucket, S3 APIs proved all four public-access-block flags true, versioning Enabled, encryption AES256, expected Project tag and Sydney location. Each EC2 exercise waited for AWS instance status checks, confirmed t3.micro/running/expected VPC and tags, checked HTTP/SSH restricted to the reviewed /32, and fetched `HTTP 200` with body `DevOps homework` from that new instance's own public IP. See `s19-http.txt` and `final-http.txt` plus their API response artifacts.

Cleanup used a reviewed destroy plan restricted to that exercise's newly created Terraform addresses/IDs. Terraform state is empty afterward. Independent AWS checks confirm three buckets return 404, two instances are terminated, both temporary VPCs return InvalidVpcID.NotFound, and their root disks return InvalidVolume.NotFound. Expected nonzero AWS CLI absence results are successful absence proof, not hidden failures. Existing RelayDesk remained ACTIVE.

The execution helper initially treated missing local state as an error; its empty-state preflight was corrected before deployment. Its cleanup address check also needed to distinguish the read-only availability-zone data source from managed AWS resources. Resumption requires exact equality of managed IDs to the new IDs recorded by this run; no ownership check was bypassed. Initial diagnostics and later successful command results are retained. Partial failures were not relabeled as successful checks.

All output is real CLI/HTTP evidence. No browser/app capture surface was available, so no new screenshot or recording is claimed. Historical plan snapshots keep `applied: false` as of their preparation time; current execution is this directory's `summary.json`. State files, plan binaries and private inputs remain ignored by Git and Docker.

`execution-helper.py` preserves this machine's one-off execution/resumption helper for provenance. It is not a general deployment command; do not rerun it or reapply stale saved plans without a new plan review and owner authorization.
