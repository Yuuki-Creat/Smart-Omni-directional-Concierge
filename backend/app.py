# API Endpoints for Smart Omni-directional Concierge
from flask import Flask, request, jsonify
from flask_cors import CORS
import service

app = Flask(__name__)
CORS(app)

# 個人向けAPI
@app.route('/api/individual/checkin', methods=['POST'])
def api_individual_checkin():
    success, data = service.process_individual_checkin(request.json)
    if success:
        return jsonify({"status": "success", "data": data}), 200
    return jsonify({"status": "error", "message": "Failed to save data"}), 500

# 法人向けAPI
@app.route('/api/corporate/status/<corp_id>', methods=['GET'])
def api_corporate_status(corp_id):
    data = service.get_corporate_status(corp_id)
    return jsonify({"status": "success", "data": data}), 200

# 工場向けAPI
@app.route('/api/factory/schedule', methods=['GET'])
def api_factory_schedule():
    data = service.calculate_factory_schedule()
    return jsonify({"status": "success", "data": data}), 200

# 店舗向けAPI
@app.route('/api/store/reception', methods=['POST'])
def api_store_reception():
    req_data = request.json
    data = service.process_store_reception(req_data.get('ticket_id'))
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
