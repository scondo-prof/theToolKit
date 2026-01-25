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