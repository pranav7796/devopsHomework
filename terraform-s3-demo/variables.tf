variable "aws_region" {
  description = "AWS region for the bucket"
  type        = string
  default     = "ap-southeast-2"
}
variable "bucket_name" {
  description = "Globally unique S3 bucket name"
  type        = string
}
variable "environment" {
  description = "Resource environment tag"
  type        = string
  default     = "homework"
}
