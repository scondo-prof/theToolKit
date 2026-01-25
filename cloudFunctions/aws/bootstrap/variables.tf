variable "s3_backend_bucket" {
  type        = string
  description = "The S3 bucket to store the Terraform state."
}

variable "s3_backend_key" {
  type        = string
  description = "The S3 key to store the Terraform state."
}

variable "project" {
  type        = string
  description = "The project name. Used for resource naming and tagging."
}

variable "environment" {
  type        = string
  description = "The environment name (e.g., dev, staging, prod). Used for resource naming and tagging."
}

variable "aws_region" {
  type        = string
  description = "The AWS region to deploy the bootstrap resources to."
  default     = "us-east-1"
}

variable "owner" {
  type        = string
  description = "The owner of the project. Used for resource naming and tagging."
}

variable "ecr_image_tag_mutability" {
  type        = string
  description = "Image tag mutability for the ECR repository. Valid values: MUTABLE or IMMUTABLE."
  default     = "MUTABLE"
  validation {
    condition     = contains(["MUTABLE", "IMMUTABLE"], var.ecr_image_tag_mutability)
    error_message = "ecr_image_tag_mutability must be either MUTABLE or IMMUTABLE."
  }
}

variable "ecr_repository_names" {
  type        = list(string)
  description = "List of ECR repository names to create. Each name will be prefixed with '{environment}-{project}-'."
  default     = []
}
