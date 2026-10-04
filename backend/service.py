# Service layer for Smart Omni-directional Concierge application
import random

from repository import save_data, fetch_data
import uuid

# 工場の1日のスケジュール（時間枠）を生成・取得
def get_daily_schedule(db):
    if "hourly_schedule" not in db:
        schedule = []
        for hour in range(9, 21):
            b2b_load = random.randint(30, 70)
            schedule.append({
                "time": f"{hour}:00",
                "capacity": 100,
                "b2b_load": b2b_load,
                "b2c_load": 0,
                "b2c_items": []
            })
        db["hourly_schedule"] = schedule
    return db["hourly_schedule"]

# 個人向け(B2C)処理
def process_individual_checkin(req_data):
    req_data['ticket_id'] = f"IND-{str(uuid.uuid4())[:6].upper()}"
    req_data['user_type'] = 'individual'

    # オフピーク誘導を判定
    if 'オフピーク' in str(req_data.get('visit_time', '')):
        req_data['granted_points'] = 500
        req_data['priority'] = 'low'
    else:
        req_data['granted_points'] = 0
        req_data['priority'] = 'high'

    db = fetch_data()

    if 'individuals' not in db:
        db['individuals'] = []
    req_data['status'] = '受付前'
    db['individuals'].append(req_data)

    schedule = get_daily_schedule(db)

    best_slot = max(schedule, key=lambda s: s["capacity"] - s["b2b_load"] - s["b2c_load"])

    quantity = req_data.get('quantity', 1)
    if (best_slot["capacity"] - best_slot["b2b_load"] - best_slot["b2c_load"]) >= quantity:
        best_slot["b2c_load"] += quantity
        best_slot["b2c_items"].append(req_data['ticket_id'])

    is_saved = save_data(db)

    return is_saved, req_data

# 法人向け(B2B)処理
def get_corporate_status(corp_id):
    db = fetch_data()
    corporates = db.get("corporates", [])

    for corp in corporates:
        if corp.get("corp_id") == corp_id:
            return corp

    return {
        "corp_id": corp_id, 
        "uniforms_in_factory": 0, 
        "next_delivery_date": "未定"
    }

# 工場向け(factory)処理
def calculate_factory_schedule():
    db = fetch_data()
    schedule = get_daily_schedule(db)

    total_b2b = sum(s["b2b_load"] for s in schedule)
    total_b2c = sum(s["b2c_load"] for s in schedule)
    total_capacity = sum(s["capacity"] for s in schedule)
    
    available_slots = total_capacity - total_b2b - total_b2c

    individuals = db.get("individuals", [])
    b2c_pending = len([item for item in individuals if item.get("status") == "受付前"])

    if available_slots < (total_capacity * 0.1):  # 空き枠が総容量の10%未満の場合
        status = "warning"
    else:
        status = "stable"

    return {
        "base_load": total_b2b, 
        "b2c_pending": b2c_pending, 
        "available_slots": available_slots if available_slots > 0 else 0,
        "status": status,
        "hourly_schedule": schedule
    }

# 店舗向け(store)処理
def process_store_reception(ticket_id):
    db = fetch_data()
    
    individuals = db.get("individuals", [])
    for item in individuals:
        if item.get("ticket_id") == ticket_id:
            item["status"] = "店舗受付完了"
            save_data(db)
            return {"status": "success", "message": f"{ticket_id} のお預かりを完了しました。"}
    # QRコード読み取り後の受付完了処理
    return {"status": "success", "message": f"{ticket_id} のお預かりを完了しました。"}
