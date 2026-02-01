# EventBridge Schedules GitHub Actions Workflow Lambda

AWS Lambda function that handles events from Amazon EventBridge and triggers GitHub Actions workflow_dispatch events using the GitHub REST API.

## Overview

This Lambda function is designed to be triggered by Amazon EventBridge events. When invoked, it triggers a GitHub Actions workflow_dispatch event via the GitHub REST API, enabling automated workflow runs based on EventBridge events or schedules.

**Current Implementation**: The function triggers the `github-issues-discord-integration.yml` workflow in the `scondo-prof/the_ticketing_system` repository, which runs periodic issue updates that send Discord notifications.

## Architecture

- **Trigger**: Amazon EventBridge (scheduled events or custom event patterns)
- **Runtime**: Python 3.12
- **Deployment**: Docker container
- **HTTP Client**: `httpx` library for making synchronous HTTP requests to GitHub API
- **Target**: GitHub Actions workflow_dispatch event via GitHub REST API

## Function Structure

The Lambda function is structured as follows:

```
eventbridge_schedules_github_actions_web_request/
├── main.py              # Main Lambda handler function
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image definition
├── README.md           # This file
└── terraform/          # Terraform infrastructure as code
    ├── main.tf         # Main Terraform configuration
    ├── variables.tf    # Variable definitions
    ├── outputs.tf      # Output definitions
    └── config/         # Configuration files
        ├── utils.tfvars         # Variable values (project, environment, owner)
        └── utils-backend.tfvars # S3 backend configuration
```

## Handler Function

The main handler function receives EventBridge events and triggers GitHub Actions workflows. On each invocation it first calls `load_secrets_manager_environment_variables()` to load configuration from the secret identified by `SECRET_ARN` into the environment, then reads GitHub and workflow settings from env vars and triggers the workflow:

```python
def main(event: dict, context: dict) -> dict:
    """Main Lambda handler function for EventBridge-triggered GitHub Actions workflow dispatch.

    Args:
        event (dict): The EventBridge event payload (may contain optional 'inputs' key)
        context (dict): The Lambda context object

    Returns:
        dict: Lambda response with statusCode and body containing GitHub API response
    """
```

### GitHub Workflow Dispatch Function

The function also includes a reusable helper for triggering workflows:

```python
def trigger_github_workflow_dispatch(
    owner: str, repo: str, workflow_id: str, github_token: str, 
    ref: str = "main", inputs: dict | None = None
) -> dict:
    """Trigger a GitHub Actions workflow_dispatch event via the GitHub REST API.

    Returns 204 status code on successful workflow trigger.
    """
```

## Dependencies

The function uses:

- **`httpx`** – HTTP client for calling the GitHub REST API
- **`boto3`** – AWS SDK for reading secrets from AWS Secrets Manager in `load_secrets_manager_environment_variables()`

See `requirements.txt` for the full dependency list.

## EventBridge Event Format

The function receives events in the standard EventBridge format:

```json
{
  "version": "0",
  "id": "event-id",
  "detail-type": "Event Detail Type",
  "source": "event.source",
  "account": "123456789012",
  "time": "2024-01-01T00:00:00Z",
  "region": "us-east-1",
  "detail": {
    // Event-specific details
  }
}
```

## Usage

### Local Development

To test the function locally:

```bash
python main.py
```

### Building the Docker Image

Build the Docker image for deployment:

```bash
docker build -t eventbridge-schedules-web-request .
```

### Deployment

Deploy this Lambda function using Terraform infrastructure as code:

#### Terraform Deployment

The project uses Terraform to deploy the Lambda function and associated EventBridge resources. The S3 backend is declared as `backend "s3" {}`; config is supplied via `-backend-config`.

1. **Configure Backend**: Set up `terraform/config/utils-backend.tfvars` with backend attributes:
   ```hcl
   bucket = "your-terraform-state-bucket"
   key    = "utils/root/eventbridge_schedules_github_actions_web_request.tfstate"
   region = "us-east-1"
   ```

2. **Configure Variables**: Set up `terraform/config/utils.tfvars`:
   ```hcl
   project     = "gh-issues"
   environment = "root"
   owner       = "scondo-prof"
   ```

3. **Initialize Terraform**:
   ```bash
   cd terraform
   terraform init -backend-config=config/utils-backend.tfvars
   ```

4. **Plan and Apply**:
   ```bash
   terraform plan -var-file=config/utils.tfvars
   terraform apply -var-file=config/utils.tfvars
   ```

#### Manual Deployment

Alternatively, deploy manually using the Docker image:

1. Push the image to Amazon ECR
2. Create or update the Lambda function to use the container image
3. Configure EventBridge to trigger the Lambda function

## Infrastructure as Code (Terraform)

This project uses Terraform to manage the AWS infrastructure. The Terraform configuration uses a reusable module for EventBridge-scheduled Lambda functions.

### Terraform Module

The configuration uses the `eventbridge_schedule_ecr_container_lambda` module from the `useful-iac` repository:

```hcl
module "eventbridge_schedule_ecr_container_lambda" {
  source = "git::https://github.com/your-org/useful-iac.git//eventbridge_schedule_ecr_container_lambda?ref=7-eventbridge-ecr-lambda"
}
```

This module handles:
- Lambda function creation with ECR container image
- EventBridge rule configuration
- IAM roles and permissions
- CloudWatch Logs configuration
- Tagging and resource naming

### Terraform Variables

#### Required Variables

- **`project`**: The project name (used for resource naming and tagging)
- **`environment`**: The deployment environment (e.g., `root`, `test`, `staging`, `production`)
- **`owner`**: The owner of the resources (used for tagging)
- **`name_prefix`**: Prefix for Lambda and related resource names (e.g., `gh-actions-web-request`)

#### Optional Variables

- **`aws_region`**: The AWS region to deploy resources to (default: `us-east-1`)

Backend (`bucket`, `key`, `region`) is configured via `-backend-config` only, not via variables.

### Terraform Backend Configuration

The S3 backend is declared as `backend "s3" {}` in `main.tf`. Configure it via `-backend-config` (e.g. `config/utils-backend.tfvars`) using backend attributes:

```hcl
bucket = "your-terraform-state-bucket"
key    = "utils/root/eventbridge_schedules_github_actions_web_request.tfstate"
region = "us-east-1"
```

### Terraform Provider Configuration

The AWS provider is configured with default tags that are applied to all resources:

```hcl
default_tags {
  tags = {
    Environment = var.environment
    Project     = var.project
    Owner       = var.owner
  }
}
```

### Configuration Files

- **`terraform/config/utils.tfvars`**: Variable values (project, environment, owner)
- **`terraform/config/utils-backend.tfvars`**: S3 backend configuration (bucket, key, region)

## Configuration

### EventBridge Rule

Configure an EventBridge rule to trigger this Lambda function:

1. Create an EventBridge rule with your desired event pattern (handled by Terraform module)
2. Set the target to this Lambda function (handled by Terraform module)
3. Ensure the Lambda function has the necessary permissions to be invoked by EventBridge (handled by Terraform module)

### Lambda Permissions

The Lambda function needs permission to be invoked by EventBridge. The Terraform module automatically configures:

- Lambda resource-based policy to allow EventBridge invocations
- EventBridge rule target configuration
- IAM roles and policies for Lambda execution

If deploying manually, ensure the function's resource-based policy includes:

```json
{
  "Effect": "Allow",
  "Principal": {
    "Service": "events.amazonaws.com"
  },
  "Action": "lambda:InvokeFunction",
  "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME"
}
```

## GitHub Actions Workflow Requirements

The target GitHub Actions workflow must have `workflow_dispatch` defined in its trigger configuration:

```yaml
on:
  workflow_dispatch:  # Required for manual API triggers
    # Optional: define inputs here if you want to pass parameters
```

**Important**: If the workflow's `workflow_dispatch` trigger doesn't define `inputs`, do not pass inputs in the API call. Doing so will result in a 422 error. The function currently works with workflows that don't define inputs (like the default target workflow).

## Response Codes

The function returns standard HTTP status codes:

- **204**: Workflow dispatch triggered successfully (GitHub API returns 204 No Content on success)
- **400**: Missing required environment variable (GITHUB_TOKEN) - validation error before API call
- **404**: Workflow not found - check repository, workflow file name, and branch
- **422**: Invalid inputs - workflow's `workflow_dispatch` doesn't accept the provided inputs
- **500**: Network error or request failure - connection issues or timeout

**Success Indicator**: When the function successfully triggers a workflow, it receives a 204 status code from GitHub's API and returns `{"statusCode": 204, "body": {"status_code": 204, "message": "Workflow dispatch triggered successfully", "success": True}}`.

## Extending the Function

To trigger different workflows or add additional functionality:

1. Modify environment variables to point to different repositories/workflows
2. Extract additional data from the EventBridge event payload
3. Add conditional logic based on event type or content
4. Implement retry logic for failed requests
5. Add logging to CloudWatch for better observability

The function uses synchronous `httpx.post()` which is ideal for single HTTP requests in Lambda.

## Environment Variables

Configure these environment variables in the Lambda function settings (or via Terraform `environment_variables` / `lambda_secret_variables`).

### Required:
- **SECRET_ARN**: ARN of the AWS Secrets Manager secret containing runtime configuration. The secret must be a JSON object whose keys are environment variable names and values are the variable values (e.g. `{"GITHUB_TOKEN": "ghp_..."}`). The handler calls `load_secrets_manager_environment_variables()` at startup to load these into `os.environ`.
- **GITHUB_TOKEN**: GitHub Personal Access Token with `actions:write` permission (typically stored in the secret above)
  - Create at: GitHub Settings → Developer settings → Personal access tokens
  - Required scope: `actions:write` to trigger workflows

### Optional (with defaults):
- **GITHUB_OWNER**: Repository owner (default: `scondo-prof`)
- **GITHUB_REPO**: Repository name (default: `the_ticketing_system`)
- **GITHUB_WORKFLOW**: Workflow file name (default: `github-issues-discord-integration.yml`)
- **GITHUB_BRANCH**: Branch or tag to trigger from (default: `main`)

### Secrets Manager Loading

The handler calls `load_secrets_manager_environment_variables()` at the start of each invocation. It reads the secret identified by `SECRET_ARN`, parses it as JSON, and sets each key-value pair as an environment variable. This allows sensitive values (e.g. `GITHUB_TOKEN`) to be stored in Secrets Manager and injected at runtime without embedding them in Terraform or the container image.

## Logging

The function logs events and context using `print()` statements. In a Lambda environment, these logs will appear in CloudWatch Logs.

## Monitoring

Monitor the function's execution through:

- **CloudWatch Logs**: View function execution logs
- **CloudWatch Metrics**: Monitor invocation counts, duration, errors
- **AWS X-Ray**: Enable tracing for detailed performance analysis

## Requirements

### Runtime Requirements

- Python 3.12
- Docker (for containerized deployment)
- AWS CLI configured (for deployment)
- EventBridge rule configured to trigger the function

### Infrastructure Requirements

- **Terraform** >= 1.0.0
- **AWS Provider** ~> 6.0
- **S3 Backend**: An S3 bucket for storing Terraform state
- **Terraform Module Access**: Access to the `useful-iac` repository containing the `eventbridge_schedule_ecr_container_lambda` module
- **AWS Credentials**: Configured AWS credentials with permissions to create:
  - Lambda functions
  - EventBridge rules
  - IAM roles and policies
  - CloudWatch Log Groups
  - ECR repositories (if pushing Docker images)

## Related Documentation

- [AWS Lambda with Docker](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/)
- [httpx Documentation](https://www.python-httpx.org/)
