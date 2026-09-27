# repository data access layer for Smart Omni-directional Concierge application
import json
import os
import requests

# Render環境変数からGist ID、GitHubトークン、GitHub URLを取得
GIST_ID = os.environ.get("GIST_ID")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_URL = os.environ.get("GITHUB_URL")

# Gistへデータを保存
def save_data(data, filename="db.json"):
    url = f"{GITHUB_URL}/{GIST_ID}"
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

# データ処理をカプセル化
def fetch_data(filename="db.json"):
    url = f"{GITHUB_URL}/{GIST_ID}"
    response = requests.get(url)
    if response.status_code == 200:
        gist_data = response.json()
        content = gist_data.get('files', {}).get(filename, {}).get('content', '{}')
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

    return {
        "individuals": [],
        "corporates": [],
        "factory_status": {}
    }
