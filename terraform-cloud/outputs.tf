output "instance_public_ip" { value = aws_instance.demo.public_ip }
output "bucket_name" { value = aws_s3_bucket.artifacts.id }
output "vpc_id" { value = aws_vpc.project.id }
