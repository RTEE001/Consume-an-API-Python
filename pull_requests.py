import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  
TOKEN = os.getenv("TOKEN")

def check_user(owner):   
    
    if (requests.get(f"https://api.github.com/users/{owner}",auth=({owner}, TOKEN))).status_code!=200:
        raise Exception ("User Not Found")
    else:
        return True
    
def check_repo(owner, repo_name):
    
    if check_user(owner):
        if (requests.get(f"https://api.github.com/repos/{owner}/{repo_name}",auth=({owner}, TOKEN))).status_code!=200:
            raise Exception("Repo Not Found")
        else:
            return True      

def get_pull_requests(owner, repo_name, start_date, end_date): 
    
    if (check_user(owner) and check_repo(owner,repo_name)):
    
        url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls?state=all"
        url_response = requests.get(url, auth=({owner}, TOKEN))
        repos = url_response.json()
        pull_details = []
        another_page= True
        
        while another_page:
            json_data = json.dumps(repos, indent=4)
            python_data = json.loads(json_data)
            
            for each_object in python_data:
                if start_date <= each_object.get("created_at")[:10] <= end_date:
                    if each_object.get("id") in [item["id"] for item in pull_details]:
                        pass
                    else:
                        pull_details.append(
                        {
                            "id": each_object.get("id"),
                            "user": each_object.get("user")["login"],
                            "title": each_object.get("title"),
                            "state": each_object.get("state"),
                            "created_at": each_object.get("created_at")[:10],
                        }
                    )
                        
            if "next" in url_response.links.keys():         
                url_response = requests.get(url_response.links["next"]["url"])
                repos.extend(url_response.json())
                
            else:
                another_page = False
                
        return pull_details
