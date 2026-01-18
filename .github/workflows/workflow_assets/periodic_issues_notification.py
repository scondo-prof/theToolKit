from datetime import datetime
import json
import os

import httpx


def format_and_send_to_discord(issues_file_path: str = "issues.json", github_repository: str | None = None) -> bool:
    """Format GitHub issues data and send Discord messages in batches.

    Reads issues from a JSON file, formats them into Discord-compatible markdown
    messages, and sends them directly to Discord. Messages are sent in batches of
    3 issues per message to avoid Discord message length limits.

    Args:
        issues_file_path: Path to the JSON file containing issues data.
            Defaults to "issues.json". The file must contain a list of issue
            dictionaries with the following keys:
            - 'number': Issue number
            - 'title': Issue title
            - 'state': Issue state (e.g., 'open', 'closed')
            - 'user': Dictionary with 'login' key for creator username
            - 'created_at': ISO format creation timestamp
            - 'updated_at': ISO format last update timestamp
            - 'html_url': URL to the issue on GitHub
        github_repository: GitHub repository in the format "owner/repo" (e.g.,
            "scondo-prof/the_ticketing_system"). If None, attempts to read from
            the GITHUB_REPOSITORY environment variable. If not available,
            defaults to an empty string (links will be omitted).

    Returns:
        bool: True if all messages were sent successfully sent.

    Note:
        - Only open issues (state != 'closed') are included in the message body.
        - Closed issues are counted separately for the summary.
        - Messages are sent in batches of 3 issues to prevent Discord message limits.
        - The "Total Open Issues" and "Total Closed Issues" labels are clickable
          links that navigate to the repository's filtered issues pages on GitHub.
        - Requires DISCORD_WEBHOOK_URL environment variable to be set.
    """

    discord_message: str = f"""---
# _Issues as of {datetime.now().strftime('%Y-%m-%d')}_
---------------------------------------------------
"""

    # Get GitHub repository from parameter or environment variable
    if github_repository is None:
        github_repository = os.getenv("GITHUB_REPOSITORY", "")

    # Issu Data Source
    with open(issues_file_path, "r", encoding="utf-8") as issues_file:
        issues: list[dict] = json.load(issues_file)

    total_closed_issues: int = 0
    total_open_issues: int = 0

    issue_send_cutoff: int = 0
    for issue in issues:
        if issue["state"] == "closed":
            total_closed_issues += 1
        else:
            total_open_issues += 1
            issue_send_cutoff += 1

            discord_message += f"""
## Issue Title: {issue['number']} - {issue['title']}

__Issue State__: `{issue['state']}`
__Created By__: `{issue['user']['login']}`
__Issue Created At__: `{issue['created_at']}`
__Issue Last Update__: `{issue['updated_at']}`
"""
        if issue_send_cutoff >= 3:
            send_to_discord(discord_message)
            discord_message = ""
            issue_send_cutoff = 0

    discord_message += f"""

[__Total Open Issues__](https://github.com/{github_repository}/issues?q=is%3Aissue%20state%3Aopen): `{total_open_issues}`
[__Total Closed Issues__](https://github.com/{github_repository}/issues?q=is%3Aissue%20state%3Aclosed): `{total_closed_issues}`
---------------------------------------------------
"""
    send_to_discord(discord_message)
    return True


def send_to_discord(discord_message: str) -> None:
    """Send a formatted message to Discord via webhook.

    Sends a markdown-formatted message to Discord using the webhook URL specified
    in the DISCORD_WEBHOOK_URL environment variable.

    Args:
        discord_message: The formatted Discord message string to send. Should
            be in Discord markdown format.

    Raises:
        Exception: If DISCORD_WEBHOOK_URL is not set or if the Discord API
            returns a non-204 status code.

    Note:
        - Expects DISCORD_WEBHOOK_URL environment variable to be set.
        - Uses httpx for HTTP POST requests.
        - Successful response status code is 204 (No Content).
        - Prints success/failure messages to stdout for workflow logging.
    """
    discord_webhook_url: str | None = os.getenv("DISCORD_WEBHOOK_URL")
    if discord_webhook_url is None:
        raise Exception("DISCORD_WEBHOOK_URL is not set")

    headers = {"Content-Type": "application/json"}
    data = {"content": discord_message}
    response = httpx.post(discord_webhook_url, headers=headers, json=data)
    if response.status_code == 204:
        print(f"Message sent to Discord successfully: {response.status_code}")
    else:
        print(f"Failed to send message to Discord: {response.status_code}")
        print(response.text)
        raise Exception(f"Failed to send message to Discord: {response.status_code} - {response.text}")


if __name__ == "__main__":
    format_and_send_to_discord()
