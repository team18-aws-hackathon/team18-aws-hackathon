output "frontend_bucket_name" {
  description = "Name of the frontend S3 bucket"
  value       = aws_s3_bucket.frontend.bucket
}

output "frontend_bucket_website_endpoint" {
  description = "Website endpoint for frontend S3 bucket"
  value       = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

output "backend_bucket_name" {
  description = "Name of the backend S3 bucket"
  value       = aws_s3_bucket.backend.bucket
}

output "lambda_role_arn" {
  description = "ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_role.arn
}

output "lambda_role_name" {
  description = "Name of the Lambda execution role"
  value       = aws_iam_role.lambda_role.name
}