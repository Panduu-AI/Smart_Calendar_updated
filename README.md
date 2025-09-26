
Smart Calendar Project (generated from your uploaded CSV)
============================================================

This package was created from the uploaded CSV and contains a demo-ready AI-driven slot recommender.

Contents:
- ai_service/: Flask app serving POST /suggest using RandomForest model
- slot_recommender.pkl: trained model
- smart_calendar_ml_ready.csv: ML-ready dataset (derived from your uploaded CSV)
- train/: script to retrain the model
- scheduler/: demo scheduler to call AI service (reminders)
- migrations/: SQL for DB schema
- frontend_demo/: small HTML to call /suggest
- requirements.txt, .env.example, Dockerfile, README.md

How to run (local):
1. Create venv and install:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
2. Start AI service:
   cd ai_service
   python app.py
3. Test with frontend_demo or run scheduler demo:
   cd ../scheduler
   python scheduler.py

Files derived from uploaded CSV: saved as smart_calendar_ml_ready.csv in project root.
