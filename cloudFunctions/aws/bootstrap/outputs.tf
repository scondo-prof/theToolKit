output "cloud_functions_ecr_repository_url" {
  value = module.aws_bootstrap.ecr_repository_urls[0]
}

output "cloud_functions_ecr_repository_arn" {
  value = module.aws_bootstrap.ecr_repository_arns[0]
}

output "cloud_functions_ecr_repository_name" {
  value = module.aws_bootstrap.ecr_repository_names[0]
}
