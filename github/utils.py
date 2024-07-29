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
        return repos
            
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        print(response.json())
        return {}
    

def get_repository_names_urls(repos: list) -> dict:
    repo_names_urls = {}

    for repo in repos:
        repo_names_urls[repo["name"]] = repo["html_url"]
    
    return repo_names_urls
    


    

def main():
    secrets = json.loads(os.getenv("github_secrets"))

    token = secrets["token"]
    org = secrets["org"]
    
    repos = get_github_repositories(token=token, org=org)

    repo_names_urls = get_repository_names_urls(repos=repos)

    print(repo_names_urls)
    
    



if __name__ == "__main__":
    main()
