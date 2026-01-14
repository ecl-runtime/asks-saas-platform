import requests
import json
from datetime import datetime

BACKEND_URL = "https://asks-backend.onrender.com"

def send_objection_handler(recipient_email, company_name, objection_type="cost"):
    if objection_type == "cost":
        message = f"""I get it. Five grand is money.

But let's do the math: If one runaway process costs you 10k and we prevent that once, we paid for ourselves. You're probably due for one soon.

We can also do $499/month if you want to test it first. Same kill-switch logic.

-ASKS"""
    elif objection_type == "engineering":
        message = f"""Right. Your team thinks they can monitor this themselves.

They probably can. But they won't. Monitoring is boring. Runaway processes happen at 2am on a Sunday.

We automate the boring part.

-ASKS"""
    else:
        message = "How can we help move this forward?"
    
    log_payload = {
        "agent_name": "Agent 5 - Objections",
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
    result = send_objection_handler("founder@company.com", "TechCorp", "cost")
    print(json.dumps(result, indent=2))
