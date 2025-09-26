# train/train_model.py
import pandas as pd, joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
df = pd.read_csv("../smart_calendar_ml_ready.csv", parse_dates=["start_time","end_time"])
X = df[["hour","day_of_week","workload","no_show_prob","patient_pref"]]
y = df["success"]
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X_train,y_train)
print(classification_report(y_test, model.predict(X_test)))
print("AUC:", roc_auc_score(y_test, model.predict_proba(X_test)[:,1]))
joblib.dump(model, "../slot_recommender.pkl")
print("Saved model to ../slot_recommender.pkl")
