# Smart-Omni-directional-Concierge

- 1.起動手順
 - URLをクリック
 - https://smart-omni-directional-concierge-frontend.onrender.com
 - ※backendの起動はRenderの設定でStartCommandを定義
  - gunicorn app:app(WebServer filename:args)

- 2.使用技術
 - Vue 3
 - Python,Flask
 - PWA(デモ用)
 - QR(模擬)
 - GitHub Gists(デモ用)

- 3.AIと用途
 - AI -> 使用
  - 使用用途
   - 案だし・案練り直し(チャット形式：壁打ち相手)
   - ソースサンプル
   - エラー時の調査補助
   - 資料骨子作成

- 4.未実装部分・注意点
 - 未実装部分
  - 認証、権限情報
  - DB構築
  - 最適化処理(動的価格、ポイント処理など)
 
 - 注意点
  - Render(動的・静的サイトのデプロイサービス)をFreeで使用しているため、
  - 初回起動、バックエンド処理が15分以上経過すると、バックエンドの処理が１分ほどかかる

- 5.ロジックツリー
- project-root/
- │
- ├── frontend/                         # フロントエンド (Vue 3)
- │   ├── package.json                  # 依存関係定義
- │   ├── vite.config.js                # Vueコードの翻訳許可
- │   ├── index.html                    # アプリ展開用
- │   └── src/
- │       ├── App.vue                   # メインコンポーネント（画面のルーティング：顧客(個人・法人)、店舗、工場のルートボタンを定義）
- │       ├── api/
- │       │   └── apiClient.js          # API通信モジュール（Pythonとの通信処理をカプセル化）
- │       │
- │       └── components/               # 4つのロールに応じたUIコンポーネント群
- │           ├── client/               # 【サービスを利用する側】
- │           │   ├── IndividualUI.vue  # 個人向け：事前カルテ入力、QRコード発行、オフピーク予約
- │           │   └── CorporateUI.vue   # 法人向け：契約ステータス、工場預かり状況の確認ダッシュボード
- │           │
- │           └── staff/                # 【サービス提供】
- │               ├── FactoryDash.vue   # 工場向け：法人ベースロードと個人の空き枠を可視化する平準化エンジン
- │               └── StoreRecp.vue     # 店舗受付向け：QRコード読取、スマート受付完了処理
- │
- └── backend/                          # バックエンド (Python / Flask)
-     ├── requirements.txt              # 依存関係定義 (Flask, requests, flask-cors 等)
-     │
-     ├── app.py                        # 【ルーティング層】
-     │                                 # 個人・法人・工場・店舗それぞれに向けた4つのAPIエンドポイント（URL）を提供
-     │
-     ├── service.py                    # 【サービス層】
-     │                                 # B2C向けデータ取得処理、B2Bのステータス取得、工場の稼働枠計算などのビジネスロジック
-     │
-     └── repository.py                 # 【リポジトリ層】
-                                       # GitHub Gist（疑似DB）とのデータ保存・取得処理
-                                       # （将来AWS等へ移行する際はこのファイルのみを修正する疎結合設計）
