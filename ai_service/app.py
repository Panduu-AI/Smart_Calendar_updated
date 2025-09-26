# ai_service/app.py
from flask import Flask, request, jsonify
import os, joblib, traceback
from datetime import datetime, timedelta
app = Flask(__name__)
MODEL_PATH = os.getenv("MODEL_PATH", "slot_recommender.pkl")
model = None
try:
    model = joblib.load(MODEL_PATH)
    app.logger.info("Model loaded")
except Exception as e:
    app.logger.warning(f"Model load failed: {e}")
def score_slot(slot_dt, workload_dict, no_show_dict, client_pref_hour=None):
    hour = slot_dt.hour
    dow = slot_dt.weekday()
    wkld = workload_dict.get(str(hour), workload_dict.get(hour, 0))
    no_show = no_show_dict.get(str(hour), no_show_dict.get(hour, 0.2))
    pref_flag = False
    if client_pref_hour is not None:
        pref_flag = abs((hour + slot_dt.minute/60.0) - client_pref_hour) <= 1.0
    features = [[hour, dow, wkld, no_show, int(pref_flag)]]
    try:
        if model is not None:
            return float(model.predict_proba(features)[0][1])
    except Exception as e:
        app.logger.warning(f"Model predict failed: {e}\\n{traceback.format_exc()}")
    pref_score = 1.0 if pref_flag else 0.0
    workload_score = max(0, 1 - (wkld / 5.0))
    no_show_score = 1 - no_show
    early_bonus = max(0, (12 - hour) / 12.0)
    raw = (0.4*pref_score) + (0.25*no_show_score) + (0.2*workload_score) + (0.15*early_bonus)
    return float(raw)
def suggest_slots(payload):
    start_date = payload.get("start_date")
    end_date = payload.get("end_date")
    duration = int(payload.get("duration_minutes", 30))
    availability = payload.get("availability", [])
    busy_slots = payload.get("busy_slots", [])
    workload_dict = payload.get("workload_dict", {})
    no_show_dict = payload.get("no_show_dict", {})
    client_pref_hour = payload.get("client_pref_hour", None)
    top_k = int(payload.get("top_k", 3))
    current = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    duration_td = timedelta(minutes=duration)
    busy = [datetime.fromisoformat(x) for x in busy_slots] if busy_slots else []
    slot_scores = {}
    while current <= end:
        day_entries = []
        for a in availability:
            s = datetime.fromisoformat(a["start"])
            e = datetime.fromisoformat(a["end"])
            if s.date() == current.date():
                day_entries.append((s,e))
        if not day_entries:
            s = datetime(current.year, current.month, current.day, 9, 0)
            e = datetime(current.year, current.month, current.day, 18, 0)
            day_entries = [(s,e)]
        for s,e in day_entries:
            slot = s
            while slot + duration_td <= e:
                slot_end = slot + duration_td
                overlap = False
                for b in busy:
                    b_end = b + duration_td
                    if slot < b_end and slot_end > b:
                        overlap = True
                        break
                if overlap:
                    slot += timedelta(minutes=30)
                    continue
                score = score_slot(slot, workload_dict or {}, no_show_dict or {}, client_pref_hour)
                slot_scores[slot] = score
                slot += timedelta(minutes=30)
        current += timedelta(days=1)
    top = sorted(slot_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [{"start": s.isoformat(sep=' '), "score": float(f)} for s,f in top]
@app.route("/suggest", methods=["POST"])
def suggest_endpoint():
    try:
        payload = request.get_json()
        if not payload.get("start_date") or not payload.get("end_date"):
            return jsonify({"error":"start_date and end_date required"}), 400
        return jsonify({"suggested_slots": suggest_slots(payload)})
    except Exception as e:
        app.logger.error(f"Error: {e}\\n{traceback.format_exc()}")
        return jsonify({"error":"internal"}), 500
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT",5001)), debug=True)
