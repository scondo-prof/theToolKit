import httpx
from dotenv import load_dotenv
import os
import json

from utils import get_github_repositories

load_dotenv()

def check_repo_rulesets(org: str, token: str, repo_name: str):
    

    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = httpx.get(url, headers=headers)

    print(response.json())

def apply_repo_ruleset(repo: str):
    pass

def main():
    github_secrets = json.loads(os.getenv("github_secrets"))
    org = github_secrets["org"]
    token = github_secrets["token"]

    repos = get_github_repositories(token=token, org=org)

    for repo in repos:
        repo_name = repo["name"]

        check_repo_rulesets(org= org, token=token, repo_name= repo_name)


main()