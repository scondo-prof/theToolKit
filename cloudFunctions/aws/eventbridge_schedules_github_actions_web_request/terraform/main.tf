terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  required_version = ">= 1.0.0"
  backend "s3" {}
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

module "eventbridge_schedule_ecr_container_lambda"{
  source = "git::https://github.com/your-org/useful-iac.git//eventbridge_schedule_ecr_container_lambda?ref=7-eventbridge-ecr-lambda"

  # add variables
}