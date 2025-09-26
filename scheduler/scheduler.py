# scheduler demo
import os, requests
from datetime import date, timedelta
AI_URL = os.getenv("AI_URL", "http://localhost:5001/suggest")
def run_once():
    payload = {
        "start_date": date.today().isoformat(),
        "end_date": (date.today()+timedelta(days=7)).isoformat(),
        "duration_minutes": 30,
        "availability": [{"start": f"{date.today().isoformat()} 09:00:00", "end": f"{date.today().isoformat()} 17:00:00"}],
        "busy_slots": [], "workload_dict": {"9":2,"10":1,"11":0}, "no_show_dict": {"9":0.3,"10":0.1,"11":0.05},
        "client_pref_hour": 19, "top_k":3
    }
    r = requests.post(AI_URL, json=payload, timeout=10)
    print("AI response:", r.json())
if __name__ == "__main__":
    run_once()
