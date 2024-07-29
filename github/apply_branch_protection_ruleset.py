import httpx
from dotenv import load_dotenv
import os
import json

from utils import get_github_repositories

load_dotenv()

def check_repo_rulesets(org: str, token: str, repo_name: str) -> list:
    

    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = httpx.get(url, headers=headers)

    rules = response.json()

    return rules

def apply_repo_ruleset(repo_name: str, org: str, token: str) -> None:

    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    data = {
   "name":"main-protection",
   "target":"branch",
   "enforcement":"active",
   "bypass_actors":[
      {
         "actor_id":1,
         "actor_type":"OrganizationAdmin",
         "bypass_mode":"always"
      }
   ],
   "conditions":{
      "ref_name":{
         "exclude":[
            
         ],
         "include":[
            "~DEFAULT_BRANCH"
         ]
      }
   },
   "rules":[
      {
         "type":"deletion"
      },
      {
         "type":"non_fast_forward"
      },
      {
         "type":"pull_request",
         "parameters":{
            "required_approving_review_count":1,
            "dismiss_stale_reviews_on_push":False,
            "require_code_owner_review":False,
            "require_last_push_approval":False,
            "required_review_thread_resolution":False
         }
      },
      {
         "type":"update"
      }
   ]
}
    
    response = httpx.post(url, headers=headers, data=data)

    print(response.status_code)
    if response.status_code == 200:
        print(f"-- Successfully Added Ruleset to {repo_name} --")
    
    else:
        print(f"Failed to Add Ruleset to {repo_name} --")



def get_ruleset_info(repo_name: str, org: str, token: str, ruleset_id: str) -> dict:
    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets/{ruleset_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = httpx.get(url, headers=headers)

    print(response.json())
    return response.json()

def main() -> None:
    github_secrets = json.loads(os.getenv("github_secrets"))
    org = github_secrets["org"]
    token = github_secrets["token"]

    repos = get_github_repositories(token=token, org=org)

    for repo in repos:
        repo_name = repo["name"]
        print(f"-- Checking {repo_name} --")

        rules = check_repo_rulesets(org= org, token=token, repo_name= repo_name)

        if rules:
            has_rule = False
            for rule in rules:
                if rule["name"] == "main-protection":
                    has_rule = True
                    break
            if has_rule:
                continue   
        else:
            print(f"-- Need to Make Rule --")
            apply_repo_ruleset(repo_name=repo_name, org=org, token=token)

main()