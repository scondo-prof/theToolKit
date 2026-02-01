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

data "terraform_remote_state" "bootstrap" {
  backend = "s3"
  config = {
    bucket = var.bootstrap_terraform_state_bucket
    key    = var.bootstrap_terraform_state_key
    region = var.aws_region
  }
}

module "eventbridge_schedule_ecr_container_lambda" {
  source = "git::https://github.com/scondo-prof/useful-iac.git//eventbridge_schedule_ecr_container_lambda?ref=7-eventbridge-ecr-lambda"

  # add variables
  environment                           = var.environment
  project                               = var.project
  name_suffix                           = var.name_suffix
  lambda_secret_recovery_window_in_days = var.lambda_secret_recovery_window_in_days
  lambda_log_group_retention_in_days    = var.lambda_log_group_retention_in_days
  lambda_event_rule_cron                = var.lambda_event_rule_cron
  lambda_secret_variables               = var.lambda_secret_variables
  ecr_repository_url                    = data.terraform_remote_state.bootstrap.outputs.cloud_functions_ecr_repository_url
  ecr_image_tag                         = "gh-actions-web-request"
  environment_variables                 = var.environment_variables
  lambda_memory_size                    = var.lambda_memory_size
  lambda_reserved_concurrent_executions = var.lambda_reserved_concurrent_executions
  lambda_timeout                        = var.lambda_timeout
}