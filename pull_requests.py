import requests
import json



def get_pull_requests(owner, repo_name,start_date,end_date):
             
   api = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"

   daya = (requests.get(api)).json()

   data1 = json.dumps(daya,indent = 4)
   data = json.loads(data1)
   # print(data1)
   # print("------")
   for each in data:
          if start_date <= each.get("created_at")[:10] <= end_date:
            print(each.get("id"))
   
get_pull_requests("rtee001", "trial","2022-06-22","2022-06-23")
   