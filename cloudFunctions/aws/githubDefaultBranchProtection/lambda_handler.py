from dotenv import load_dotenv
import os
import json
import httpx
import boto3

load_dotenv()


def delete_ruleset(repo_name: str, org: str, token: str, ruleset_id: str) -> str:
    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets/{ruleset_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = httpx.delete(url, headers=headers)

    if response.status_code == 204:
        response_message = (
            f"Successfully Deleted Ruleset: {ruleset_id} From Repo: {repo_name}"
        )
        print(response_message)

    else:
        response_message = (
            f"Failed to Deleted Ruleset: {ruleset_id} From Repo: {repo_name}"
        )
        print(response_message)


def apply_repo_ruleset(repo_name: str, org: str, token: str) -> None:

    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    data = {
        "name": "main-protection",
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [
            {"actor_id": 1, "actor_type": "OrganizationAdmin", "bypass_mode": "always"}
        ],
        "conditions": {"ref_name": {"exclude": [], "include": ["~DEFAULT_BRANCH"]}},
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {
                "type": "pull_request",
                "parameters": {
                    "required_approving_review_count": 1,
                    "dismiss_stale_reviews_on_push": False,
                    "require_code_owner_review": False,
                    "require_last_push_approval": False,
                    "required_review_thread_resolution": False,
                },
            },
        ],
    }

    response = httpx.post(url, headers=headers, data=json.dumps(data))

    print(response.status_code)
    if response.status_code == 201:
        print(f"-- Successfully Added Ruleset to {repo_name} --")

    else:
        print(f"Failed to Add Ruleset to {repo_name} --")


def get_repo_rulesets(org: str, token: str, repo_name: str) -> list:

    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = httpx.get(url, headers=headers)

    rules = response.json()

    return rules


def get_github_repositories(token: str, org: str) -> list:
    repos = []
    count = 1

    url = f"https://api.github.com/orgs/{org}/repos?page={count}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = httpx.get(url, headers=headers)

    repos += response.json()

    if response.status_code == 200:
        while len(response.json()) == 30:
            count += 1
            url = f"https://api.github.com/orgs/{org}/repos?page={count}"
            response = httpx.get(url, headers=headers)
            repos += response.json()
        return repos

    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        print(response.json())
        return {}


def lambda_handler(event: dict, context: dict) -> None:
    sm = boto3.client("secretsmanager")
    github_secrets = json.loads(
        sm.get_secret_value(SecretId=os.getenv("github_secrets"))["SecretString"]
    )
    org = github_secrets["org"]
    token = github_secrets["token"]

    repos = get_github_repositories(token=token, org=org)

    for repo in repos:
        repo_name = repo["name"]
        print(f"-- Checking {repo_name} --")

        rules = get_repo_rulesets(org=org, token=token, repo_name=repo_name)

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
                delete_ruleset(
                    repo_name=repo_name, org=org, token=token, ruleset_id=ruleset_id
                )
                print(f"-- Making Rule for Repo: {repo_name} --")

        else:
            print(f"-- Making Rule for Repo: {repo_name} --")
            apply_repo_ruleset(repo_name=repo_name, org=org, token=token)
