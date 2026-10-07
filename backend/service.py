# Service layer for Smart Omni-directional Concierge application
import random

from repository import save_data, fetch_data
import uuid

# 工場の1日のスケジュール（時間枠）を生成・取得
def get_daily_schedule(db):
    if "hourly_schedule" not in db:
        schedule = []
        # 9時から20時までの時間枠を生成
        for hour in range(9, 21):
            # ランダムなB2B負荷を生成（30〜70の範囲）：デモ用
            b2b_load = random.randint(30, 70)
            schedule.append({
                "time": f"{hour}:00",
                "capacity": 100,        # 各時間枠の最大容量を100に設定
                "b2b_load": b2b_load,   # ランダムなB2B負荷
                "b2c_load": 0,          # B2C負荷：初期値は0
                "b2c_items": []         # B2CのチケットIDを格納するリスト
            })
        db["hourly_schedule"] = schedule
    # 生成したスケジュールを返却
    return db["hourly_schedule"]

# 個人向け(B2C)処理　チェックイン
def process_individual_checkin(req_data):
    # ユニークなチケットIDを生成し、個人向けチケットを生成(上6桁　例: IND-1A2B3C)
    req_data['ticket_id'] = f"IND-{str(uuid.uuid4())[:6].upper()}"
    req_data['user_type'] = 'individual'

    # オフピーク誘導を判定
    if 'オフピーク' in str(req_data.get('visit_time', '')):
        req_data['granted_points'] = 500    # 500ポイント付与(デモ用)
        req_data['priority'] = 'low'        # 優先度低判定
    else:
        req_data['granted_points'] = 0      # ポイントなし
        req_data['priority'] = 'high'       # 通常優先度

    # 現在のデータを取得
    db = fetch_data()

    if 'individuals' not in db:
        db['individuals'] = []
    
    # 状態を受付前にしてリストに追加
    req_data['status'] = '受付前'
    db['individuals'].append(req_data)

    # 工場のスケジュールを取得
    schedule = get_daily_schedule(db)

    # すべての時間帯の中で一番開いている時間を探索
    # （最大容量 - 法人負荷 - 個人負荷）が一番大きい枠を best_slot とする
    best_slot = max(schedule, key=lambda s: s["capacity"] - s["b2b_load"] - s["b2c_load"])

    # 個人の量を取得
    quantity = req_data.get('quantity', 1)
    
    # 一番空いている枠に個人の枠を差し込み
    if (best_slot["capacity"] - best_slot["b2b_load"] - best_slot["b2c_load"]) >= quantity:
        best_slot["b2c_load"] += quantity
        best_slot["b2c_items"].append(req_data['ticket_id'])

    is_saved = save_data(db)

    # 保存成功結果と処理済みチェックインデータを返却
    return is_saved, req_data

# 法人向け(B2B)処理　ステータス取得
def get_corporate_status(corp_id):
    db = fetch_data()
    corporates = db.get("corporates", [])

    for corp in corporates:
        if corp.get("corp_id") == corp_id:
            return corp

    # 法人IDデータが見つからない場合ダミーデータを返却
    return {
        "corp_id": corp_id, 
        "uniforms_in_factory": 0, 
        "next_delivery_date": "未定"
    }

# 工場向け(factory)処理　空き状況の計算処理
def calculate_factory_schedule():
    db = fetch_data()
    schedule = get_daily_schedule(db)

    # スケジュール全体のB2B、B2C、最大容量を計算
    total_b2b = sum(s["b2b_load"] for s in schedule)
    total_b2c = sum(s["b2c_load"] for s in schedule)
    total_capacity = sum(s["capacity"] for s in schedule)
    
    # 全体の空き容量を計算
    available_slots = total_capacity - total_b2b - total_b2c

    # 受付前の個人件数を取得
    individuals = db.get("individuals", [])
    b2c_pending = len([item for item in individuals if item.get("status") == "受付前"])

    # 空き枠が総容量の10%未満の場合warning
    if available_slots < (total_capacity * 0.1):
        status = "warning"
    else:
        status = "stable"

    # 計算した工場の全体状況データを返却
    return {
        "base_load": total_b2b, 
        "b2c_pending": b2c_pending, 
        "available_slots": available_slots if available_slots > 0 else 0,
        "status": status,
        "hourly_schedule": schedule
    }

# 店舗向け(store)処理　受付処理
def process_store_reception(ticket_id):
    db = fetch_data()
    
    individuals = db.get("individuals", [])
    # 該当するチケットIDの個人データを検索し、ステータスを「店舗受付完了」に更新
    for item in individuals:
        if item.get("ticket_id") == ticket_id:
            item["status"] = "店舗受付完了"
            save_data(db)
            # QRコード読み取り後の受付完了処理
            return {"status": "success", "message": f"{ticket_id} のお預かりを完了しました。"}
    # 該当するチケットIDが見つからない場合でも成功メッセージを返却(デモ用)
    return {"status": "success", "message": f"{ticket_id} のお預かりを完了しました。"}
