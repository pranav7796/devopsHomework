# Terraform S3 Demo

Creates a private, versioned S3 bucket with server-side encryption. The included `terraform.tfvars` supplies only a public bucket name so the assignment's exact file structure is present. Change it if AWS reports a name collision. Do not add credentials to that file. The `.gitignore` excludes state and local values outside this public example.

```sh
terraform init
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
terraform show
terraform output
terraform destroy
```

**Authenticated plan verified on 21 October 2026 (IST): 4 to add, 0 to change, 0 to destroy.** [Actual plan](../evidence/aws-plans/s18-plan.txt). The reviewed plan was subsequently applied and its S3 controls verified, then destroyed; AWS confirmed bucket absence. [Execution evidence](../evidence/aws-execution/README.md). The provider defaults to Sydney and rejects accounts other than `525426877661`. Use the existing CLI login with the [reviewed credential/workflow instructions](../AWS-HOMEWORK.md); never put credentials in tfvars. Remote state and state locking are not configured in this learning demo.

[Terminal screenshot of the saved execution/cleanup logs](../evidence/screenshots-2026-10-21/s18-evidence.png), captured on 21 October 2026 (IST), shows apply/destroy totals, S3 controls and bucket absence. [Capture provenance](../evidence/screenshots-2026-10-21/README.md).
