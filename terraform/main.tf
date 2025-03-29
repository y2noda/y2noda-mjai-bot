provider "aws" {
  region = var.aws_region
}

# S3バケット
resource "aws_s3_bucket" "model_artifacts" {
  bucket = "${var.project_name}-artifacts"
  tags   = var.tags
}

resource "aws_s3_bucket_versioning" "model_artifacts" {
  bucket = aws_s3_bucket.model_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

# SageMaker用のIAMロール
resource "aws_iam_role" "sagemaker_role" {
  name = "${var.project_name}-sagemaker-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
      }
    ]
  })

  tags = var.tags
}

# SageMaker用のポリシー
resource "aws_iam_role_policy" "sagemaker_policy" {
  name = "${var.project_name}-sagemaker-policy"
  role = aws_iam_role.sagemaker_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.model_artifacts.arn,
          "${aws_s3_bucket.model_artifacts.arn}/*"
        ]
      }
    ]
  })
}

# SageMakerノートブックインスタンス
resource "aws_sagemaker_notebook_instance" "training" {
  name          = "${var.project_name}-training"
  role_arn      = aws_iam_role.sagemaker_role.arn
  instance_type = var.instance_type

  tags = var.tags
}
