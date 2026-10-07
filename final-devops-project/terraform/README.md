# Final project Terraform

This is the Session 21 copy of the Session 19 AWS demo configuration. It provisions a VPC, public subnet, Internet Gateway, route table, security group restricted to the supplied CIDR, EC2 HTTP demo and private S3 bucket. The working Session 19 exercise remains in `../../terraform-cloud/`.

Create a local `terraform.tfvars` containing `ami_id`, globally unique `bucket_name`, and `ssh_cidr` before planning. Supply AWS credentials through a secure environment or profile. Review resource costs and the plan before any apply.

```sh
terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
terraform show
terraform output
terraform destroy
```

The local configuration was validated; it was not applied to AWS. Do not commit state, plans, credentials or a populated `terraform.tfvars`.
