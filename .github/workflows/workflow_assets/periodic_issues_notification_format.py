from datetime import datetime
import json
import os

discord_message = f"""---
# _Issues as of {datetime.now().strftime('%Y-%m-%d')}_
---------------------------------------------------
"""

with open("issues.json", "r", encoding="utf-8") as issues_file:
    issues = json.load(issues_file)

total_closed_issues = 0
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

# GitHub provides the path to the outputs file here:
output_path = os.environ["GITHUB_OUTPUT"]

# Write a multiline output
with open(output_path, "a", encoding="utf-8") as f:
    f.write("discord_message<<EOF\n")
    f.write(discord_message)
    f.write("\nEOF\n")

print("Wrote discord_message to GITHUB_OUTPUT")
