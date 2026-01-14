import requests
import json
from datetime import datetime

BACKEND_URL = "https://asks-backend.onrender.com"

def send_followup_1(recipient_email, company_name):
    message = f"""Quick follow-up, {company_name.split()}.

Did my previous message land? No pressure if it's not a priority right now.

But if you've had any late-night scares about API bills, we should talk. That's literally the only problem we solve.

Let me know.

-ASKS"""
    
    log_payload = {
        "agent_name": "Agent 3 - Follow-up 1",
        "recipient_email": recipient_email,
        "message": message,
        "response_status": "sent"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/agent/log", json=log_payload)
        return {
            "success": response.status_code == 200,
            "recipient": recipient_email,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    result = send_followup_1("founder@company.com", "TechCorp")
    print(json.dumps(result, indent=2))
