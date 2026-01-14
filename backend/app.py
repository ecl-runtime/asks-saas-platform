from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
import hashlib

app = Flask(__name__)
CORS(app)

BUDGET_DATA_FILE = "budget_data.json"

def load_budget_data():
    if os.path.exists(BUDGET_DATA_FILE):
        with open(BUDGET_DATA_FILE, 'r') as f:
            return json.load(f)
    return {"budgets": [], "spent": []}

def save_budget_data(data):
    with open(BUDGET_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "ASKS backend is running", "timestamp": datetime.now().isoformat()})

@app.route('/api/intent', methods=['POST'])
def capture_intent():
    data = request.get_json()
    company_name = data.get('company_name', 'Unknown')
    monthly_spend = data.get('monthly_spend', 0)
    email = data.get('email', '')
    
    budget_data = load_budget_data()
    intent_entry = {
        "id": hashlib.md5(f"{email}{datetime.now().isoformat()}".encode()).hexdigest(),
        "company_name": company_name,
        "monthly_spend": monthly_spend,
        "email": email,
        "timestamp": datetime.now().isoformat(),
        "status": "captured"
    }
    budget_data["budgets"].append(intent_entry)
    save_budget_data(budget_data)
    
    return jsonify({"success": True, "intent_id": intent_entry["id"], "message": "Intent captured. Agent team incoming."})

@app.route('/api/budget/check', methods=['POST'])
def check_budget():
    data = request.get_json()
    current_spend = data.get('current_spend', 0)
    budget_limit = data.get('budget_limit', 5000)
    
    if current_spend >= budget_limit:
        return jsonify({"status": "BLOCKED", "message": "Budget limit reached. Calls stopped.", "spend": current_spend, "limit": budget_limit})
    
    percentage = (current_spend / budget_limit) * 100
    return jsonify({"status": "ACTIVE", "spend": current_spend, "limit": budget_limit, "percentage": percentage})

@app.route('/api/budgets', methods=['GET'])
def get_budgets():
    data = load_budget_data()
    return jsonify(data)

@app.route('/api/agent/log', methods=['POST'])
def log_agent_interaction():
    data = request.get_json()
    agent_name = data.get('agent_name', 'Unknown')
    recipient_email = data.get('recipient_email', '')
    message = data.get('message', '')
    response_status = data.get('response_status', 'pending')
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "recipient": recipient_email,
        "message_preview": message[:100],
        "status": response_status
    }
    
    if os.path.exists("agent_logs.json"):
        with open("agent_logs.json", 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(log_entry)
    
    with open("agent_logs.json", 'w') as f:
        json.dump(logs, f, indent=2)
    
    return jsonify({"success": True, "log_id": log_entry["timestamp"]})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=int(port), debug=False)
