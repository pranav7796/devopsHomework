variable "aws_region" {
  type    = string
  default = "ap-south-1"
}
variable "ami_id" {
  type        = string
  description = "Region-specific Linux AMI ID"
}
variable "bucket_name" {
  type        = string
  description = "Globally unique S3 bucket name"
}
variable "ssh_cidr" {
  type        = string
  description = "Your public IP as CIDR, e.g. 203.0.113.4/32"
  validation {
    condition     = can(cidrhost(var.ssh_cidr, 0))
    error_message = "ssh_cidr must be a valid CIDR."
  }
}
