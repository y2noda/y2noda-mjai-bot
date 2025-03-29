output "notebook_instance_url" {
  description = "URL of the SageMaker notebook instance"
  value       = "https://${aws_sagemaker_notebook_instance.training.name}.notebook.${var.aws_region}.sagemaker.aws.amazon.com"
}

output "model_artifacts_bucket" {
  description = "Name of the S3 bucket for model artifacts"
  value       = aws_s3_bucket.model_artifacts.id
}

output "sagemaker_role_arn" {
  description = "ARN of the IAM role used by SageMaker"
  value       = aws_iam_role.sagemaker_role.arn
}
