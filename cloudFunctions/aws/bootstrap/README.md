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

Use `config/utils-backend.tfvars` (or your own backend file) to set the S3 backend:

```hcl
s3_backend_bucket = "your-terraform-state-bucket"
s3_backend_key    = "bootstrap.tfstate"
```

State path used by the backend: `{project}/{environment}/{s3_backend_key}.tfstate`

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
terraform plan -var-file=config/utils.tfvars \
  -var="s3_backend_bucket=your-bucket" \
  -var="s3_backend_key=bootstrap.tfstate" \
  -var="owner=your-name"
terraform apply -var-file=config/utils.tfvars \
  -var="s3_backend_bucket=your-bucket" \
  -var="s3_backend_key=bootstrap.tfstate" \
  -var="owner=your-name"
```

Adjust `-var` and `-var-file` to match your backend and environment.

## Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `s3_backend_bucket` | string | yes | — | S3 bucket for Terraform state. |
| `s3_backend_key` | string | yes | — | S3 object key for state file. |
| `project` | string | yes | — | Project name; used for naming and tags. |
| `environment` | string | yes | — | Environment (e.g. `dev`, `staging`, `root`). |
| `owner` | string | yes | — | Owner; used for tagging. |
| `aws_region` | string | no | `us-east-1` | AWS region for bootstrap resources. |
| `ecr_image_tag_mutability` | string | no | `MUTABLE` | `MUTABLE` or `IMMUTABLE` for ECR image tags. |
| `ecr_repository_names` | list(string) | no | `[]` | ECR repository names. Prefixed with `{environment}-{project}-`. |

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
