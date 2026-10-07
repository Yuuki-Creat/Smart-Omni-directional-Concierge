# repository data access layer for Smart Omni-directional Concierge application
import json
import logging
import os
import requests

# Render環境変数からGist ID、GitHubトークン、GitHub URLを取得
GIST_ID = os.environ.get("GIST_ID")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_URL = os.environ.get("GITHUB_URL")

# Gistへデータを保存する関数
def save_data(data, filename="db.json"):
    # URL作成
    url = f"{GITHUB_URL}/{GIST_ID}"
    # ヘッダーとペイロードを設定
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
    # Gistにデータを保存するPATCHリクエストを送信
    response = requests.patch(url, headers=headers, json=payload)
    return response.status_code == 200

# データをGistから取得する関数
def fetch_data(filename="db.json"):
    # URL作成
    url = f"{GITHUB_URL}/{GIST_ID}"
    # ヘッダーを設定
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        # Gistからデータを取得
        response = requests.get(url, headers=headers)
        # ステータスコードが200でない場合は例外を発生
        response.raise_for_status()
        gist_data = response.json()
        # Gistのファイル内容を取得(content)し、JSONで返却
        content = gist_data.get('files', {}).get(filename, {}).get('content', '{}')
        return json.loads(content)
    # 通信エラー、JSONデコードエラーをキャッチしてログに記録
    except (requests.RequestException, json.JSONDecodeError) as e:
            logging.info(f"Error fetching data: {e}")
            # Gistからの取得に失敗した場合は、空のデータを返却
            return {
                "individuals": [],
                "corporates": [],
                "factory_status": {}
            }
