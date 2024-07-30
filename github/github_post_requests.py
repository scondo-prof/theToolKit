import httpx
import json

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
      }
   ]
}
    
    response = httpx.post(url, headers=headers, data=json.dumps(data))

    print(response.status_code)
    if response.status_code == 201:
        print(f"-- Successfully Added Ruleset to {repo_name} --")
    
    else:
        print(f"Failed to Add Ruleset to {repo_name} --")