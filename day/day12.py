import requests
def fetch_github_user(username):
    url=f"https://api.github.com/users/{username}"
    try:
        response=requests.get(url,timeout=5)
        if response.status_code==200:
            return response.json().get("name",username)
        return None
    except requests.exceptions.Timeout:
        print("请求超时")