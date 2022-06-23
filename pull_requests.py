import requests
import json

def get_pull_requests(owner, repo_name, start_date, end_date):

      api = f"https://api.github.com/repos/{owner}/{repo_name}/pulls?state=all"
      raw_data = (requests.get(api)).json()
      data1 = json.dumps(raw_data)
      data = json.loads(data1)
      req = []

      for each in data:
         if start_date <= each.get("created_at")[:10] <= end_date:
               req.append(
                  {
                     "id": each.get("id"),
                     "user": each.get("user")["login"],
                     "title": each.get("title"),
                     "state": each.get("state"),
                     "created_at": each.get("created_at")[:10],
                  }
               )
      return json.dumps(req, indent = 4)

print(get_pull_requests("Umuzi-org", "ACN-syllabus", "2022-03-01", "2022-03-10"))
