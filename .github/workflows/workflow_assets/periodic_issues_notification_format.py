from datetime import datetime
import json
import os

discord_message = f"""
---
# Issues as of {datetime.now().strftime('%Y-%m-%d')}
---------------------------------------------------
"""
with open("issues.json", "r") as issues_file:
    issues = json.load(issues_file)

    for issue in issues:
        issue_message = f"""


## Issue Title: {issue['number']} - {issue['title']}

Issue State: {issue['state']}

Created By: {issue['user']['login']}

![Avatar]({issue['user']['avatar_url']})

Issue Created At: {issue['created_at']}
Issue Last Update: {issue['updated_at']}

[Issue Link]({issue['html_url']})
 """
        discord_message += issue_message

os.environ["GITHUB_OUTPUT"] = f"discord_message=test"

print(f" This is the GITHUB_OUTPUT: {os.getenv('GITHUB_OUTPUT')}")
