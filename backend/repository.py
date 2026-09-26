import json
import os
import requests

# Render環境変数からGist ID、GitHubトークン、GitHub URLを取得
GIST_ID = os.environ.get("GIST_ID")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_URL = os.environ.get("GITHUB_URL")

# Gistへデータを保存
def save_to_gist(data, filename="db.json"):
    url = f"{GITHUB_URL}/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "files": {
            filename: {
                "content": json.dumps(data, indent=4, ensure_ascii=False)
            }
        }
    }
    response = requests.patch(url, headers=headers, json=payload)
    return response.status_code == 200
