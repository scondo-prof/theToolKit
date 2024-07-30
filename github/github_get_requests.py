import httpx

def get_ruleset_info(repo_name: str, org: str, token: str, ruleset_id: str) -> dict:
    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets/{ruleset_id}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = httpx.get(url, headers=headers)

    ruleset_info = response.json()

    return ruleset_info

def get_repo_rulesets(org: str, token: str, repo_name: str) -> list:
    

    url = f"https://api.github.com/repos/{org}/{repo_name}/rulesets"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = httpx.get(url, headers=headers)

    rules = response.json()

    return rules