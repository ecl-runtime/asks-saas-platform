import requests
import json
from datetime import datetime

BACKEND_URL = "https://asks-backend.onrender.com"

def send_cold_email(recipient_email, company_name, monthly_spend):
    message = f"""Hi {company_name.split()},

I noticed you're doing {monthly_spend}k/month in API spend.

If you're running agents or batch jobs, there's probably a runaway process waiting to happen. One errant loop = $30k bill before you notice.

We built a kill-switch for this. Hard stops the calls when you hit budget.

$5k to install. 48 hours.

Worth a conversation?

-ASKS Team"""
    
    log_payload = {
        "agent_name": "Agent 1 - Cold",
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
    result = send_cold_email("founder@company.com", "TechCorp", 15)
    print(json.dumps(result, indent=2))
