from datetime import datetime
import json
import os

import httpx


def format_discord_message(issues_file_path: str = "issues.json") -> str:
    """Format GitHub issues data into a Discord message string.

    Reads issues from a JSON file and formats them into a Discord-compatible
    markdown message. Includes open issues with their details (title, state,
    creator, creation date, last update) and a summary of total closed issues.

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

    Returns:
        str: Formatted Discord message containing:
            - Header with current date
            - Details for each open issue
            - Footer with total count of closed issues

    Note:
        Only open issues (state != 'closed') are included in the message body.
        Closed issues are only counted for the summary.
    """

    discord_message: str = f"""---
    # _Issues as of {datetime.now().strftime('%Y-%m-%d')}_
    ---------------------------------------------------
    """

    # Issu Data Source
    with open(issues_file_path, "r", encoding="utf-8") as issues_file:
        issues: list[dict] = json.load(issues_file)

    total_closed_issues: int = 0
    for issue in issues:
        if issue["state"] == "closed":
            total_closed_issues += 1
        else:

            discord_message += f"""
## Issue Title: {issue['number']} - {issue['title']}

__Issue State__: `{issue['state']}`
__Created By__: `{issue['user']['login']}`
__Issue Created At__: `{issue['created_at']}`
__Issue Last Update__: `{issue['updated_at']}`
## [Issue Link]({issue['html_url']})
"""

    discord_message += f"""

__Total Closed Issues__: `{total_closed_issues}`
---------------------------------------------------
"""
    return discord_message


if __name__ == "__main__":
    print(format_discord_message())
