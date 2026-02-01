import httpx
import json
import os

import boto3


sm = boto3.client("secretsmanager")


def load_secrets_manager_environment_variables() -> bool:
    try:
        print("Loading secrets manager environment variables")
        secret_variables: dict[str, str] = json.loads(
            sm.get_secret_value(SecretId=os.getenv("SECRET_ARN"))["SecretString"]
        )
        for secret_variable in secret_variables:
            os.environ[secret_variable] = secret_variables[secret_variable]
        print("Secrets manager environment variables loaded")
        return True
    except Exception as e:
        print(f"Error loading secrets manager environment variables: {e}")
        return False


def trigger_github_workflow_dispatch(
    owner: str, repo: str, workflow_id: str, github_token: str, ref: str = "main", inputs: dict | None = None
) -> dict:
    """Trigger a GitHub Actions workflow_dispatch event via the GitHub REST API.

    This function makes an HTTP POST request to GitHub's API to trigger a workflow_dispatch event,
    which manually starts a GitHub Actions workflow. The target workflow must have `workflow_dispatch`
    defined in its trigger configuration.

    Note: If the target workflow's `workflow_dispatch` trigger doesn't define inputs, passing inputs
    will result in a 422 error. Only include inputs if the workflow explicitly defines them under
    `workflow_dispatch.inputs`.

    Args:
        owner: Repository owner (e.g., 'scondo-prof')
        repo: Repository name (e.g., 'the_ticketing_system')
        workflow_id: Workflow file name (e.g., 'github-issues-discord-integration.yml')
        github_token: GitHub Personal Access Token with 'actions:write' permission
        ref: Branch or tag name to trigger the workflow from (default: 'main')
        inputs: Optional workflow inputs dictionary. Only use if the workflow defines inputs under
                `workflow_dispatch`. If None or empty, no inputs will be sent.

    Returns:
        dict: Response dictionary containing:
            - status_code (int): HTTP status code from GitHub API
            - message (str): Human-readable message about the result
            - success (bool): True if workflow was triggered successfully (204 status)
            - response_body (str, optional): Error response body if request failed
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }

    payload = {"ref": ref}
    if inputs:
        payload["inputs"] = inputs

    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=30.0)

        if response.status_code == 204:
            return {
                "status_code": response.status_code,
                "message": "Workflow dispatch triggered successfully",
                "success": True,
            }
        else:
            return {
                "status_code": response.status_code,
                "message": f"Error: {response.text}",
                "success": False,
                "response_body": response.text,
            }
    except httpx.RequestError as e:
        return {"status_code": 500, "message": f"Request error: {str(e)}", "success": False}


def main(event: dict, context: dict) -> dict:
    """Main Lambda handler function for EventBridge-triggered GitHub Actions workflow dispatch.

    This function is invoked by Amazon EventBridge when a configured event rule matches. It extracts
    configuration from environment variables and optional event data, then triggers a GitHub Actions
    workflow via the GitHub REST API.

    Environment Variables:
        GITHUB_TOKEN (required): GitHub Personal Access Token with 'actions:write' permission
        GITHUB_OWNER (optional): Repository owner (default: 'scondo-prof')
        GITHUB_REPO (optional): Repository name (default: 'the_ticketing_system')
        GITHUB_WORKFLOW (optional): Workflow file name (default: 'github-issues-discord-integration.yml')
        GITHUB_BRANCH (optional): Branch/tag to trigger from (default: 'main')

    Event Format:
        The event dictionary can optionally contain:
        - inputs (dict): Workflow inputs to pass (only if workflow defines workflow_dispatch.inputs)

    Args:
        event (dict): The EventBridge event payload. May contain:
            - inputs (dict, optional): Workflow inputs to pass to GitHub Actions
        context (dict): The Lambda context object containing runtime information

    Returns:
        dict: Lambda response dictionary with:
            - statusCode (int): HTTP status code (200, 400, or from GitHub API)
            - body (dict): Response body containing the result from trigger_github_workflow_dispatch()
    """
    print("Starting Lambda function")
    load_secrets_manager_environment_variables()
    print(f"Received EventBridge event: {event}")
    print(f"Lambda context: {context}")
    github_token: str = os.environ.get("GITHUB_TOKEN")
    owner: str = os.environ.get("GITHUB_OWNER", "scondo-prof")
    repo: str = os.environ.get("GITHUB_REPO", "the_ticketing_system")
    workflow_id: str = os.environ.get("GITHUB_WORKFLOW", "github-issues-discord-integration.yml")
    branch: str = os.environ.get("GITHUB_BRANCH", "main")

    inputs = event.get("inputs") if event else None

    if not github_token:
        return {"statusCode": 400, "body": "GITHUB_TOKEN environment variable is required"}

    result = trigger_github_workflow_dispatch(
        owner=owner, repo=repo, workflow_id=workflow_id, github_token=github_token, ref=branch, inputs=inputs
    )

    return {"statusCode": result.get("status_code", 200), "body": result}


if __name__ == "__main__":
    test_event = {}
    result = main(event=test_event, context={})
    print(f"Lambda response: {result}")
