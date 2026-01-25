terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  required_version = ">= 1.0.0"
  backend "s3" {
    bucket = var.s3_backend_bucket
    key    = "${var.project}/${var.environment}/${var.s3_backend_key}.tfstate"
    region = var.aws_region
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project
      Owner       = var.owner
    }
  }
}

module "aws_bootstrap" {
  source = "git::https://github.com/scondo-prof/useful-iac.git//aws_bootstrap?ref=16-bootstrap-ecr-module"

  environment              = var.environment
  project                  = var.project
  ecr_image_tag_mutability = var.ecr_image_tag_mutability
  ecr_repository_names     = var.ecr_repository_names
}