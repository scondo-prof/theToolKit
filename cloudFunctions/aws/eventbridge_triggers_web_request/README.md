# EventBridge Triggers Web Request Lambda

AWS Lambda function that handles events from Amazon EventBridge and can be extended to make web requests using `httpx`.

## Overview

This Lambda function is designed to be triggered by Amazon EventBridge events. The function receives events from EventBridge, processes them, and can be extended to make HTTP requests to external services or APIs.

## Architecture

- **Trigger**: Amazon EventBridge
- **Runtime**: Python 3.12
- **Deployment**: Docker container
- **HTTP Client**: `httpx` library for making web requests

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

The main handler function signature:

```python
def main(event: dict, context: dict) -> dict:
    """Main function to handle the event from the EventBridge.

    Args:
        event (dict): The event from the EventBridge.
        context (dict): The context from the EventBridge.

    Returns:
        dict: The response from the EventBridge.
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

## Extending the Function

The function currently prints the event and context, then returns a simple response. To extend it for making web requests:

1. Extract relevant data from the EventBridge event
2. Use `httpx` to make HTTP requests to your target endpoints
3. Process the responses
4. Return appropriate status codes and responses

Example extension:

```python
import httpx

async def make_web_request(url: str, data: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        return {"status_code": response.status_code, "body": response.text}
```

## Environment Variables

If needed, configure environment variables in the Lambda function settings for:

- Target API endpoints
- API keys or authentication tokens
- Configuration values

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
