# Service layer for Smart Omni-directional Concierge application
from repository import save_data, fetch_data
import uuid

# 個人向け(B2C)処理
def process_individual_checkin(req_data):
    req_data['ticket_id'] = f"IND-{str(uuid.uuid4())[:6].upper()}"
    req_data['user_type'] = 'individual'

    # オフピーク誘導を判定
    if req_data.get('visit_time') == 'オフピーク' or req_data.get('visit_time') == 'オフピーク':
        req_data['granted_points'] = 500
        req_data['priority'] = 'low'
    else:
        req_data['granted_points'] = 0
        req_data['priority'] = 'high'

    db = fetch_data()

    if 'individuals' not in db:
        db['individuals'] = []
    db['individuals'].append(req_data)

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
    corporates = db.get("corporates", [])
    base_load = sum(corp.get("uniforms_in_factory", 0) for corp in corporates)
    individuals = db.get("individuals", [])
    b2c_pending = len(individuals)

    max_capacity = 200  # 工場の最大処理能力(仮)

    available_slots = max_capacity - base_load
    
    if available_slots - b2c_pending < 20: # 空き枠から現在待機中の個人案件を引いた残りが少ない場合（ここでは20未満と仮定）
        status = "warning"
    else:
        status = "stable"
    return {
        "base_load": base_load, 
         "b2c_pending": b2c_pending, 
         "available_slots": available_slots if available_slots > 0 else 0,
         "status": status
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
