variable "aws_region" {
  description = "AWS region for the bucket"
  type        = string
  default     = "ap-south-1"
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
