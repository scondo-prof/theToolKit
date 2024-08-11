def get_repository_names_urls(repos: list) -> dict:
    repo_names_urls = {}

    for repo in repos:
        repo_names_urls[repo["name"]] = repo["html_url"]
    
    return repo_names_urls