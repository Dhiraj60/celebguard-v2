# backend/app.py

import os
import sys
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ✅ Add project root to sys.path for clean imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

from backend.db import load_contracts
from backend.scraper import check_content_live

# ✅ Enable Flask to serve frontend files
app = Flask(
    __name__,
    static_folder=os.path.join(project_root, "frontend"),
    static_url_path=""
)
CORS(app)

DATA_FILE = os.path.join(project_root, "data", "contracts.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# ➕ Add new contract
@app.route('/add_contract', methods=['POST'])
def add_contract():
    data = request.json
    try:
        with open(DATA_FILE, 'r') as f:
            contracts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        contracts = []

    contracts.append(data)

    with open(DATA_FILE, 'w') as f:
        json.dump(contracts, f, indent=4)

    return jsonify({'status': 'success', 'data': data})

# 📋 Get all contracts
@app.route('/all_contracts', methods=['GET'])
def all_contracts():
    contracts = load_contracts()
    return jsonify({'contracts': contracts})

# 🛡️ Check all status
@app.route('/check_all_status', methods=['GET'])
def check_all_status():
    contracts = load_contracts()
    result = []

    for c in contracts:
        expiry = datetime.strptime(c["expiry_date"], "%Y-%m-%d")
        status = "expired" if expiry < datetime.now() else "active"
        live = check_content_live(c["content_link"]) if status == "expired" else True

        result.append({
            **c,
            "status": status,
            "still_live": live
        })

    return jsonify({"contracts": result})

# 🌐 Serve index.html (UI)
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# 🌐 Serve contract form UI
@app.route('/contract_form')
def serve_contract_form():
    return send_from_directory(app.static_folder, 'contract_form.html')

# 🛠️ Run server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
