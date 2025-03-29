variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "ap-northeast-1"
}

variable "project_name" {
  description = "Project name to be used for resource naming"
  type        = string
  default     = "mjai-bot"
}

variable "instance_type" {
  description = "SageMaker notebook instance type"
  type        = string
  default     = "ml.t3.medium"  # 開発用の小さめのインスタンス
}

variable "tags" {
  description = "Tags to be applied to all resources"
  type        = map(string)
  default = {
    Project     = "mjai-bot"
    Environment = "dev"
  }
}
