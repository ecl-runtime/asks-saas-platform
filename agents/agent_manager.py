import json
import os
import sys
from datetime import datetime

sys.path.insert(0, '/Users/yourname/Desktop/asks-day1/agents')

try:
    from agent_1_cold_outreach import send_cold_email
    from agent_3_followup_1 import send_followup_1
    from agent_5_objections import send_objection_handler
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all agent files are in the same directory")
    sys.exit(1)

LEADS_FILE = "leads.json"

def load_leads():
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leads(leads):
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2)

def run_all_agents():
    print("=== ASKS Agent Manager Started ===")
    print(f"Time: {datetime.now().isoformat()}")
    print()
    
    leads = load_leads()
    
    if not leads:
        print("No leads loaded. Using sample data.")
        leads = [
            {"email": "founder@example.com", "company": "TechStartup", "spend": 15},
            {"email": "cto@another.com", "company": "AICompany", "spend": 25},
        ]
        save_leads(leads)
    
    print(f"Total leads: {len(leads)}")
    print()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "agent_1_cold": [],
        "agent_3_followup": [],
        "agent_5_objections": [],
        "summary": {}
    }
    
    print("--- Agent 1: Cold Outreach ---")
    for lead in leads[:5]:
        result = send_cold_email(lead['email'], lead['company'], lead['spend'])
        results["agent_1_cold"].append(result)
        status = "✓ SENT" if result['success'] else "✗ FAILED"
        print(f"{status} → {lead['email']}")
    print()
    
    print("--- Agent 3: Follow-up 1 ---")
    for lead in leads[5:10]:
        result = send_followup_1(lead['email'], lead['company'])
        results["agent_3_followup"].append(result)
        status = "✓ SENT" if result['success'] else "✗ FAILED"
        print(f"{status} → {lead['email']}")
    print()
    
    print("--- Agent 5: Objection Handler ---")
    for lead in leads[10:15]:
        result = send_objection_handler(lead['email'], lead['company'], "cost")
        results["agent_5_objections"].append(result)
        status = "✓ SENT" if result['success'] else "✗ FAILED"
        print(f"{status} → {lead['email']}")
    print()
    
    results["summary"] = {
        "total_leads": len(leads),
        "agent_1_sent": len(results["agent_1_cold"]),
        "agent_3_sent": len(results["agent_3_followup"]),
        "agent_5_sent": len(results["agent_5_objections"]),
        "expected_replies_6pct": round(len(leads) * 0.06),
        "expected_closes_50pct": round((len(leads) * 0.06) * 0.5)
    }
    
    with open("agent_run_log.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print("=== Summary ===")
    print(f"Total leads: {results['summary']['total_leads']}")
    print(f"Agent 1 cold emails: {results['summary']['agent_1_sent']}")
    print(f"Expected 6% reply rate: {results['summary']['expected_replies_6pct']} replies")
    print(f"Expected 50% close rate: {results['summary']['expected_closes_50pct']} closes")
    print(f"Expected Week 1 revenue (4 x $5k): ${results['summary']['expected_closes_50pct'] * 5000}")
    print()
    print("Log saved to agent_run_log.json")

if __name__ == "__main__":
    run_all_agents()
