import httpx
from dotenv import load_dotenv
import os
import json

load_dotenv()



def get_github_repositories(token: str,org: str) -> list:
    repos = []
    count = 1

    url = f"https://api.github.com/orgs/{org}/repos?page={count}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    response = httpx.get(url, headers=headers)

    repos += response.json()
    
    if response.status_code == 200:
        while len(response.json()) == 30:
            count += 1
            url = f"https://api.github.com/orgs/{org}/repos?page={count}"
            response = httpx.get(url, headers=headers)
            repos += response.json()
        print(len(repos))
        return repos
            
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        print(response.json())
        return None
    

def main():
    secrets = json.loads(os.getenv("github_secrets"))

    token = secrets["token"]
    org = secrets["org"]
    
    repositories = get_github_repositories(token=token, org=org)
    
    if repositories:
        for repo in repositories:
            print(f"- {repo['name']} ({repo['html_url']})")



if __name__ == "__main__":
    main()
