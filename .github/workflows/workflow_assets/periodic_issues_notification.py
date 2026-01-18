from datetime import datetime
import json
import os

import httpx


def get_gh_issues(github_repository: str | None = None, desired_issue_state: str = "all") -> list[dict]:
    """Get GitHub issues from the repository with pagination support.

    Fetches all issues from the repository by automatically handling pagination.
    Uses per_page=100 to maximize items per request and follows Link headers
    to fetch all pages.

    Args:
        github_repository: GitHub repository in the format "owner/repo" (e.g.,
            "scondo-prof/the_ticketing_system"). If None, attempts to read from
            the GITHUB_REPOSITORY environment variable. If not available,
            defaults to an empty string.
        desired_issue_state: The state of issues to retrieve. Valid values are
            "open", "closed", or "all". Defaults to "all".

    Returns:
        list[dict]: A list of all issues from all pages combined.

    Raises:
        Exception: If the GitHub API returns a non-200 status code.

    Note:
        - Automatically handles pagination to fetch all issues.
        - Uses per_page=100 to minimize the number of API requests.
        - Requires GITHUB_TOKEN environment variable to be set.
    """
    # Get GitHub repository from parameter or environment variable
    if github_repository is None:
        github_repository: str = os.getenv("GITHUB_REPOSITORY", "")

    all_issues: list[dict] = []
    page: int = 1
    per_page: int = 100

    headers: dict[str, str] = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
    }

    while True:
        url: str = (
            f"https://api.github.com/repos/{github_repository}/issues"
            f"?state={desired_issue_state}&page={page}&per_page={per_page}"
        )

        response: httpx.Response = httpx.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to get GitHub issues: {response.status_code} - {response.text}")

        page_issues: list[dict] = response.json()

        # If no issues returned, we've reached the end
        if not page_issues:
            break

        all_issues.extend(page_issues)

        # If we got fewer items than per_page, we're definitely on the last page
        if len(page_issues) < per_page:
            break

        # Check Link header for "next" rel to see if there are more pages
        link_header: str | None = response.headers.get("Link")
        has_next: bool = False

        if link_header:
            # Parse Link header to check for "next" rel
            links = link_header.split(",")
            for link in links:
                if 'rel="next"' in link:
                    has_next = True
                    break

        # If no "next" link found, we're done (even if we got a full page)
        if not has_next:
            break

        # Move to next page
        page += 1

    print(f"Retrieved {len(all_issues)} issues across {page} page(s)")
    return all_issues


def format_and_send_to_discord(issues: list[dict], github_repository: str | None = None) -> bool:
    """Format GitHub issues data and send Discord messages in batches.

    Takes a list of issue dictionaries, formats them into Discord-compatible markdown
    messages, and sends them directly to Discord. Messages are sent in batches of
    3 issues per message to avoid Discord message length limits.

    Args:
        issues: A list of issue dictionaries with the following keys:
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
# `Open Issues` _as of_ `{datetime.now().strftime('%Y-%m-%d')}`
---------------------------------------------------
"""

    # Get GitHub repository from parameter or environment variable
    if github_repository is None:
        github_repository: str = os.getenv("GITHUB_REPOSITORY", "")

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
            discord_message: str = ""
            issue_send_cutoff: int = 0

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

    headers: dict[str, str] = {"Content-Type": "application/json"}
    data: dict[str, str] = {"content": discord_message}
    response = httpx.post(discord_webhook_url, headers=headers, json=data)
    if response.status_code == 204:
        print(f"Message sent to Discord successfully: {response.status_code}")
    else:
        print(f"Failed to send message to Discord: {response.status_code}")
        print(response.text)
        raise Exception(f"Failed to send message to Discord: {response.status_code} - {response.text}")


if __name__ == "__main__":
    issues: list[dict] = get_gh_issues()
    format_and_send_to_discord(issues)
