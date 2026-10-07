# Terraform cloud demo

Illustrative AWS VPC, public subnet, Internet Gateway, route, security group, EC2 web instance and private S3 bucket. Set `ami_id`, a globally unique `bucket_name`, and your own public IP as `ssh_cidr` in a local `terraform.tfvars` file. Review every plan. The example uses one public subnet and exposes HTTP/SSH only to the supplied CIDR; it is a learning topology, not a production architecture. AWS apply/destroy have not been run. `terraform destroy` deletes the demo resources; preserve needed data first.

```sh
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
terraform show
terraform output
terraform destroy
```
