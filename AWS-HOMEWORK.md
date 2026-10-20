# Homework AWS lifecycle — verified and cleaned up

These are this repository's own exercises. RelayDesk in `helpdesk-capstone` is a separate project and is not evidence that these Terraform configurations were deployed.

## Actual verified status — 21 October 2026 (IST)

**All three exercises were applied, verified with independent AWS API/HTTP checks, and destroyed.** Terraform state is empty for each project. The three S3 buckets are absent; both new EC2 instances are terminated; both temporary VPCs and root disks are absent. RelayDesk remains ACTIVE and its cluster ARN/version/VPC are unchanged. [Execution summary](evidence/aws-execution/summary.json), [commands/output/exit codes](evidence/aws-execution/command-results.json), [verification guide](evidence/aws-execution/README.md).

Authenticated `init`, `fmt -check`, `validate`, `plan`, and saved-plan JSON inspection passed for all three projects with AWS profile `devops-new`, account `525426877661`, region `ap-southeast-2`. The Amazon Linux 2023 image was resolved from AWS's public SSM parameter. Both EC2 demos restrict HTTP and SSH to `202.131.146.146/32`.

| Project | Saved plan | Add / change / destroy | Items created temporarily and removed |
|---|---|---|---|
| Session 18 `terraform-s3-demo` | `terraform-s3-demo/tfplan-completion` | 4 / 0 / 0 | One private, encrypted, versioned S3 bucket |
| Session 19 `terraform-cloud` | `terraform-cloud/tfplan-completion` | 11 / 0 / 0 | One t3.micro EC2, its root disk/public IPv4, one S3 bucket |
| Session 21 `final-devops-project/terraform` | `final-devops-project/terraform/tfplan-completion` | 11 / 0 / 0 | Same small topology in a separate VPC and Terraform state |

The 26 planned resources include supporting routes, security groups and bucket configuration objects, not 26 separately charged servers. Each EC2 exercise has its own VPC/subnet/Internet Gateway. No NAT gateway or EKS cluster is planned. These VPCs are not peered with RelayDesk.

The owner authorized the reviewed temporary deployment/cleanup scope, and the full `apply` → live verification → deployed-state `show`/`output` → destroy workflow passed for every exercise. Original plan metadata remains a dated pre-apply snapshot; current execution/absence proof is in `evidence/aws-execution/`. Resources are no longer running.

## Reviewable evidence

- [All command exit codes and UTC timestamps](evidence/aws-plans/command-results.json).
- [Account, image, CIDR, resource addresses, private-plan hashes and source hashes](evidence/aws-plans/summary.json).
- [Session 18 plan](evidence/aws-plans/s18-plan.txt), [Session 19 plan](evidence/aws-plans/s19-plan.txt), [final-project plan](evidence/aws-plans/final-plan.txt).
- [Official AWS Price List responses](evidence/aws-plans/price-summary.json) and [AMI root-disk details](evidence/aws-plans/ami-details.json).

Plan binaries and input snapshots are ignored by Git; credentials are supplied by the AWS CLI login cache through `scripts/aws-login.config`, not stored in Terraform variables. Providers reject any AWS account other than `525426877661`. The public S3 example tfvars file contains no credentials and is overridden with an exercise-specific bucket name by the planning helper.

## Prepare or refresh the plans

From the repository root:

```bash
aws login --profile devops-new --region ap-southeast-2
aws sts get-caller-identity --profile devops-new --region ap-southeast-2
python3 scripts/prepare-aws-plans.py
```

The helper prepares all three plans but cannot apply/destroy resources. It saves private inputs under `evidence/private/aws-inputs/`. It resolves your current public IPv4 address using `checkip.amazonaws.com`; alternatively pass `--admin-cidr YOUR_PUBLIC_IPV4/32`. The read-only wrapper also rejects direct `apply`/`destroy` commands.

## Repeating the exercise requires a new reviewed approval

The execution below has already completed once, and all new homework resources were removed. Do not reapply an old saved plan: regenerate and review a fresh plan for any future run.

Review the plan/source hashes and confirm the AWS identity again. If a plan, input, account, source file or trusted IP changes, regenerate and review the plans before applying. Run the exercises sequentially so only one homework EC2 instance runs at a time.

For the approved exercise, use its directory from the table:

```bash
export AWS_CONFIG_FILE="$PWD/scripts/aws-login.config"
export AWS_PROFILE=devops-new
# Example only: run after approval of this saved plan.
terraform -chdir=terraform-s3-demo apply tfplan-completion
terraform -chdir=terraform-s3-demo show
terraform -chdir=terraform-s3-demo output
```

Save genuine output and exit codes. Independently query S3 public-access blocking, versioning and encryption. For each EC2 exercise also wait for the instance's status checks and verify its own HTTP page contains `DevOps homework`. Do not reuse RelayDesk's HTTP checks or screenshots. Capture the plan, running resource and completion evidence where a browser/terminal capture surface is available.

Before leaving each exercise, review a destroy plan using **that exercise's private input snapshot** (`s18.tfvars.json`, `s19.tfvars.json`, or `final.tfvars.json`):

```bash
# Example only: run after approval for creation and teardown of this exercise.
terraform -chdir=terraform-s3-demo plan -destroy \
  -var-file="$PWD/evidence/private/aws-inputs/s18.tfvars.json" -out=tfplan-cleanup
terraform -chdir=terraform-s3-demo apply tfplan-cleanup
```

Verify that only the newly created exercise resources were removed, then move to the next project. Do not upload objects to the buckets during this test: versioned objects would require deliberate data cleanup before bucket deletion. Never run cleanup against RelayDesk or unrelated state.

## Cost and capture limitations

The captured AWS Price List reports Sydney Linux t3.micro at USD 0.0132/hour, public IPv4 at USD 0.005/hour, and gp3 at USD 0.096/GiB-month. The selected AMI specifies an 8-GiB gp3 root disk. Using 730 hours/month, one running homework EC2 exercise is approximately **USD 0.0193/hour**, plus S3 usage/requests, transfer, any surplus CPU charges, tax and billing rounding. Both EC2 demos run concurrently would approximately double that baseline; the proposed workflow runs them sequentially. This is a dated estimate, not a bill or a credit-coverage guarantee.

Computer Use reported no app/browser surfaces. A later capture pass used the desktop's Foot/Grim tools to take [five genuine terminal screenshots](evidence/screenshots-2026-10-21/README.md), including the missing Session 19 plan and all three AWS lifecycles. These show explicitly dated saved plan/execution excerpts, not a fresh deployment or AWS Console pages. Capture commands, source/image hashes and a freshly queried CI response are retained. Existing dated screenshots retain their original dates.
