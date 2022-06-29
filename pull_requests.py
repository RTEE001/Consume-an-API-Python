import requests
import json
import os
from dotenv import load_dotenv

def get_pull_requests(owner, repo_name, start_date, end_date):
  
    load_dotenv()  
    TOKEN = os.getenv("TOKEN")
    url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls?state=all"
    url_response = requests.get(url, auth=({owner}, TOKEN))
    repos = url_response.json()
    pull_details = []

    if "message" in repos:
            print(repos["message"])
            raise Exception("Error 404 User or Repo Not Found")
    else:
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
