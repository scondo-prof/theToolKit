# AWS Cloud Functions Bootstrap

Terraform configuration that bootstraps foundational AWS resources for cloud functions in this toolkit. It provisions ECR repositories and related infrastructure via the `aws_bootstrap` module from [useful-iac](https://github.com/scondo-prof/useful-iac).

**Module source:** [useful-iac / aws_bootstrap](https://github.com/scondo-prof/useful-iac/tree/16-bootstrap-ecr-module/aws_bootstrap) (`ref=16-bootstrap-ecr-module`)

## Overview

This bootstrap runs first to create:

- **ECR repositories** – Container registries for Lambda and other container-based cloud functions
- **Tagging and naming** – Consistent `Environment`, `Project`, and `Owner` tags across resources

Other Terraform configs (e.g. Lambda, EventBridge) depend on these ECR repositories.

## Directory structure

```
bootstrap/
├── main.tf           # Provider, backend, and aws_bootstrap module
├── variables.tf      # Input variables
├── outputs.tf        # ECR URLs, ARNs, and names
├── README.md         # This file
└── config/
    ├── utils.tfvars         # Example variable values
    └── utils-backend.tfvars # Example S3 backend config
```

## Usage

### 1. Backend configuration

The S3 backend is declared as `backend "s3" {}` in `main.tf`. Config is supplied via `-backend-config` (e.g. `config/utils-backend.tfvars`). Use backend attributes, not Terraform variables:

```hcl
bucket = "your-terraform-state-bucket"
key    = "utils/root/bootstrap.tfstate"   # or your chosen path
region = "us-east-1"
```

### 2. Variable configuration

Use `config/utils.tfvars` (or your own tfvars) for environment, project, and ECR settings:

```hcl
project     = "utils"
environment = "root"
owner       = "scondo-prof"

ecr_repository_names = ["cloud-functions"]
```

### 3. Terraform commands

```bash
cd cloudFunctions/aws/bootstrap

terraform init -backend-config=config/utils-backend.tfvars
terraform plan -var-file=config/utils.tfvars
terraform apply -var-file=config/utils.tfvars
```

Use your own `-backend-config` and `-var-file` as needed. Backend settings are only in the backend config file; plan/apply use tfvars for root module variables.

## Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `project` | string | yes | — | Project name; used for naming and tags. |
| `environment` | string | yes | — | Environment (e.g. `dev`, `staging`, `root`). |
| `owner` | string | yes | — | Owner; used for tagging. |
| `aws_region` | string | no | `us-east-1` | AWS region for bootstrap resources. |
| `ecr_image_tag_mutability` | string | no | `MUTABLE` | `MUTABLE` or `IMMUTABLE` for ECR image tags. |
| `ecr_repository_names` | list(string) | no | `[]` | ECR repository names. Prefixed with `{environment}-{project}-`. |

Backend (`bucket`, `key`, `region`) is configured via `-backend-config` only, not via variables.

## Outputs

| Output | Description |
|--------|-------------|
| `ecr_repository_urls` | ECR repository URLs (for `docker push`, etc.). |
| `ecr_repository_arns` | ECR repository ARNs. |
| `ecr_repository_names` | ECR repository names. |

## Requirements

- Terraform `>= 1.0.0`
- AWS provider `~> 6.0`
- S3 bucket for Terraform state
- AWS credentials with permissions to create ECR repositories and apply default tags

## Notes

- Run this bootstrap **before** deploying Lambda or other configs that use these ECR repositories.
- ECR names are prefixed with `{environment}-{project}-`; ensure `ecr_repository_names` in this config match what other Terraform modules expect.
