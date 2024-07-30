from dotenv import load_dotenv
import os
import json

from utils import get_github_repositories
from github_get_requests import get_repo_rulesets
from github_post_requests import apply_repo_ruleset
from github_delete_requests import delete_ruleset

load_dotenv()





def main() -> None:
    github_secrets = os.getenv("github_secret")
    org = github_secrets["org"]
    token = github_secrets["token"]

    print(github_secrets)

    repos = get_github_repositories(token=token, org=org)

    for repo in repos:
        repo_name = repo["name"]
        print(f"-- Checking {repo_name} --")

        rules = get_repo_rulesets(org= org, token=token, repo_name= repo_name)

        

        if rules:
            has_rule = False
            for rule in rules:
                if rule["name"] == "main-protection":
                    has_rule = True
                    ruleset_id = rule["id"]
                    break
            if has_rule and github_secrets["overwrite"] == "No":
                print("-- Has Main Protection --")
                continue   
            elif has_rule and github_secrets["overwrite"] == "Yes":
                print("-- Has Main Protection --")
                print(f"-- Deleting Rule: {ruleset_id} From Repo: {repo_name} --")
                delete_ruleset(repo_name=repo_name, org=org, token=token, ruleset_id=ruleset_id)
                print(f"-- Making Rule for Repo: {repo_name} --")

        else:
            print(f"-- Making Rule for Repo: {repo_name} --")
            apply_repo_ruleset(repo_name=repo_name, org=org, token=token)

main()