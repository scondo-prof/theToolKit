# Generic Variables
environment = "root"
project     = "utils"
owner       = "scondo-prof"
name_suffix = "gh-actions-web-request"

# Bootstrap Variables
bootstrap_terraform_state_bucket = "scondo-iac-bucket"
bootstrap_terraform_state_key    = "utils/root/bootstrap.tfstate"

# Lambda Variables
lambda_event_rule_cron = "0 1 * * ? *"
ecr_image_tag          = "gh-actions-web-request"
