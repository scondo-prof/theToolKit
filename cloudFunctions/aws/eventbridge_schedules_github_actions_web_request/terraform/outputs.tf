# Bootstrap Remote State Outputs (from terraform_remote_state)
output "bootstrap_cloud_functions_ecr_repository_url" {
  description = "ECR repository URL from bootstrap (cloud-functions image)"
  value       = data.terraform_remote_state.bootstrap.outputs.cloud_functions_ecr_repository_url
}

output "bootstrap_cloud_functions_ecr_repository_arn" {
  description = "ECR repository ARN from bootstrap (cloud-functions image)"
  value       = data.terraform_remote_state.bootstrap.outputs.cloud_functions_ecr_repository_arn
}

output "bootstrap_cloud_functions_ecr_repository_name" {
  description = "ECR repository name from bootstrap (cloud-functions image)"
  value       = data.terraform_remote_state.bootstrap.outputs.cloud_functions_ecr_repository_name
}

# Lambda Function Outputs
output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_function_name
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_function_arn
}

output "lambda_function_invoke_arn" {
  description = "The ARN to be used for invoking Lambda function from API Gateway"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_function_invoke_arn
}

output "lambda_function_qualified_arn" {
  description = "The qualified ARN (ARN with lambda version number) of the Lambda function"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_function_qualified_arn
}

output "lambda_function_version" {
  description = "The version of the Lambda function"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_function_version
}

# Secrets Manager Outputs
output "lambda_secret_arn" {
  description = "The ARN of the Secrets Manager secret"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_secret_arn
}

output "lambda_secret_name" {
  description = "The name of the Secrets Manager secret"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_secret_name
}

# IAM Role Outputs
output "lambda_role_arn" {
  description = "The ARN of the IAM role for the Lambda function"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_role_arn
}

output "lambda_role_name" {
  description = "The name of the IAM role for the Lambda function"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_role_name
}

# CloudWatch Log Group Outputs
output "lambda_log_group_name" {
  description = "The name of the CloudWatch log group for the Lambda function"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_log_group_name
}

output "lambda_log_group_arn" {
  description = "The ARN of the CloudWatch log group for the Lambda function"
  value       = module.eventbridge_schedule_ecr_container_lambda.lambda_log_group_arn
}

# EventBridge Rule Outputs
output "eventbridge_rule_arn" {
  description = "The ARN of the EventBridge rule"
  value       = module.eventbridge_schedule_ecr_container_lambda.eventbridge_rule_arn
}

output "eventbridge_rule_name" {
  description = "The name of the EventBridge rule"
  value       = module.eventbridge_schedule_ecr_container_lambda.eventbridge_rule_name
}
