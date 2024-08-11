import httpx
from dotenv import load_dotenv
import os
import json

def delete_ruleset(repo_name: str, org: str, token: str, ruleset_id: str) -> str:
    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets/{ruleset_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = httpx.delete(url, headers=headers)

    if response.status_code == 204:
        response_message = f"Successfully Deleted Ruleset: {ruleset_id} From Repo: {repo_name}"
        print(response_message)
    
    else:
        response_message = f"Failed to Deleted Ruleset: {ruleset_id} From Repo: {repo_name}"
        print(response_message)