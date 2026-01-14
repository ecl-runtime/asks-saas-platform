import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from agent1coldoutreach import send_cold_email
from agent3followup1 import send_followup1
from agent5objections import send_objection_handler

LEADS_FILE = "leads.json"

def load_leads():
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE

