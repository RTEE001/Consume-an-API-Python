import requests
import json
import os
from dotenv import load_dotenv


def get_token():

    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    return TOKEN


def check_user(owner):

    if (
        requests.get(
            f"https://api.github.com/users/{owner}", auth=({owner}, get_token())
        )
    ).status_code != 200:
        raise Exception("User Not Found")
    else:
        return True


def check_repo(owner, repo_name):

    check_user(owner)
    if (
        requests.get(
            f"https://api.github.com/repos/{owner}/{repo_name}",
            auth=({owner}, get_token()),
        )
    ).status_code != 200:
        raise Exception("Repo Not Found")
    else:
        return True


def get_pull_requests(owner, repo_name, start_date, end_date):

    check_repo(owner, repo_name)

    url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls?state=all"
    url_response = requests.get(url, auth=({owner}, get_token()))
    repos = url_response.json()
    pull_details = []

    while True:
        for each_object in repos:
            if (
                each_object.get("created_at") != None
                and start_date <= each_object.get("created_at")[:10] <= end_date
                or (
                    each_object.get("merged_at") != None
                    and start_date <= each_object.get("merged_at")[:10] <= end_date
                )
                or (
                    each_object.get("updated_at") != None
                    and start_date <= each_object.get("updated_at")[:10] <= end_date
                )
                or (
                    each_object.get("closed_at") != None
                    and start_date <= each_object.get("closed_at")[:10] <= end_date
                )
            ):

                pull_details.append(
                    {
                        "id": each_object.get("id"),
                        "user": each_object.get("user")["login"],
                        "title": each_object.get("title"),
                        "state": each_object.get("state"),
                        "created_at": each_object.get("created_at")[:10],
                    }
                )

        if "next" not in url_response.links:
            break
        else:
            url_response = requests.get(url_response.links["next"]["url"])
            repos = url_response.json()

    return pull_details
