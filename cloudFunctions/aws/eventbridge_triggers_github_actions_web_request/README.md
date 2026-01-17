# EventBridge Triggers GitHub Actions Workflow Lambda

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
eventbridge_triggers_web_request/
├── main.py              # Main Lambda handler function
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker image definition
└── README.md           # This file
```

## Handler Function

The main handler function receives EventBridge events and triggers GitHub Actions workflows:

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

The function uses `httpx` for making HTTP requests. Key dependencies include:

- `httpx` - Modern HTTP client library for Python
- Supporting libraries: `httpcore`, `certifi`, `anyio`, `idna`, `h11`

See `requirements.txt` for the complete list of dependencies.

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
docker build -t eventbridge-triggers-web-request .
```

### Deployment

Deploy this Lambda function using the Docker image:

1. Push the image to Amazon ECR
2. Create or update the Lambda function to use the container image
3. Configure EventBridge to trigger the Lambda function

## Configuration

### EventBridge Rule

Configure an EventBridge rule to trigger this Lambda function:

1. Create an EventBridge rule with your desired event pattern
2. Set the target to this Lambda function
3. Ensure the Lambda function has the necessary permissions to be invoked by EventBridge

### Lambda Permissions

The Lambda function needs permission to be invoked by EventBridge. Ensure the function's resource-based policy includes:

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

Configure these environment variables in the Lambda function settings:

### Required:
- **GITHUB_TOKEN**: GitHub Personal Access Token with `actions:write` permission
  - Create at: GitHub Settings → Developer settings → Personal access tokens
  - Required scope: `actions:write` to trigger workflows

### Optional (with defaults):
- **GITHUB_OWNER**: Repository owner (default: `scondo-prof`)
- **GITHUB_REPO**: Repository name (default: `the_ticketing_system`)
- **GITHUB_WORKFLOW**: Workflow file name (default: `github-issues-discord-integration.yml`)
- **GITHUB_BRANCH**: Branch or tag to trigger from (default: `main`)

## Logging

The function logs events and context using `print()` statements. In a Lambda environment, these logs will appear in CloudWatch Logs.

## Monitoring

Monitor the function's execution through:

- **CloudWatch Logs**: View function execution logs
- **CloudWatch Metrics**: Monitor invocation counts, duration, errors
- **AWS X-Ray**: Enable tracing for detailed performance analysis

## Requirements

- Python 3.12
- Docker (for containerized deployment)
- AWS CLI configured (for deployment)
- EventBridge rule configured to trigger the function

## Related Documentation

- [AWS Lambda with Docker](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html)
- [Amazon EventBridge](https://docs.aws.amazon.com/eventbridge/)
- [httpx Documentation](https://www.python-httpx.org/)
