from datetime import datetime
import json
import os

discord_message = f"""---
# Issues as of {datetime.now().strftime('%Y-%m-%d')}
---------------------------------------------------
"""

with open("issues.json", "r", encoding="utf-8") as issues_file:
    issues = json.load(issues_file)

for issue in issues:
    discord_message += f"""

## Issue Title: {issue['number']} - {issue['title']}

Issue State: {issue['state']}
Created By: {issue['user']['login']}
Issue Created At: {issue['created_at']}
Issue Last Update: {issue['updated_at']}

## [Issue Link]({issue['html_url']})
"""

# GitHub provides the path to the outputs file here:
output_path = os.environ["GITHUB_OUTPUT"]

# Write a multiline output
with open(output_path, "a", encoding="utf-8") as f:
    f.write("discord_message<<EOF\n")
    f.write(discord_message)
    f.write("\nEOF\n")

print("Wrote discord_message to GITHUB_OUTPUT")
