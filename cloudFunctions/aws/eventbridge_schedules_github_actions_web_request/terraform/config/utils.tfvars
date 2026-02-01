# Generic Variables
environment = "root"
project     = "gh-issues"
owner       = "scondo-prof"
name_prefix = "gh-actions-web-request"

# Bootstrap Variables
bootstrap_terraform_state_bucket = "scondo-iac-bucket"
bootstrap_terraform_state_key = "utils/root/bootstrap.tfstate"

# Lambda Variables
lambda_event_rule_cron = "* * * * ? *"
lambda_secret_variables = { "GITHUB_TOKEN" = "github_token" }
ecr_image_tag = "gh-actions-web-request"
