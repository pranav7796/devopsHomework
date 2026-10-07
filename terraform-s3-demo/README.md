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

**Requires AWS credentials with narrowly scoped S3 bucket permissions.** No apply was run as part of this local work; never put credentials in tfvars. Remote state and state locking are not configured in this learning demo.
