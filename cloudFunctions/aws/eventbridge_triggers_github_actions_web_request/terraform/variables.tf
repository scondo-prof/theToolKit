variable "s3_backend_bucket" {
  type        = string
  description = "The S3 bucket to store the Terraform state."
}

variable "s3_backend_key" {
  type        = string
  description = "The key to store the Terraform state in the S3 bucket."
  default     = "eventbridge_trigger_ecr_container_lambda.tfstate"
}

variable "aws_region" {
  type        = string
  description = "The AWS region to deploy the resources to"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "The environment to deploy the resources to. This will be passed via CI Variables."
}

variable "project" {
  type        = string
  description = "The project name."
}

variable "owner" {
  type        = string
  description = "The owner of the resources. This will be passed via CI Variables."
}