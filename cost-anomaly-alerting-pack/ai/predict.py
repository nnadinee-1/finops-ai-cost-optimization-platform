import json
import joblib
import pandas as pd


MODEL_FILE = "cost-anomaly-alerting-pack/ai/models/random_forest_anomaly_model.pkl"
DATA_FILE = "cost-anomaly-alerting-pack/ai/processed/clean_cloud_dataset.csv"
OUTPUT_FILE = "cost-anomaly-alerting-pack/ai/output/ai_predictions.json"

model = joblib.load(MODEL_FILE)
df = pd.read_csv(DATA_FILE)

features = [
    "CPU_Usage",
    "Memory_Usage",
    "Disk_IO",
    "Network_IO",
    "Workload_Type",
    "hour",
    "day",
    "day_of_week",
]

split_index = int(len(df) * 0.8)
unseen_df = df.iloc[split_index:].copy()

sample = unseen_df[features].head(50)

predictions = model.predict(sample)
probabilities = model.predict_proba(sample)[:, 1]

results = []

for i, (_, row) in enumerate(sample.iterrows()):
    is_anomaly = int(predictions[i]) == 1
    probability = round(float(probabilities[i]), 4)

    results.append({
        "pack_name": "ai_cloud_anomaly_prediction",
        "service": row["Workload_Type"],
        "namespace": "ai-validation",
        "problem_type": "ai_predicted_cloud_anomaly",
        "severity": "high" if probability >= 0.8 else "medium" if probability >= 0.5 else "normal",
        "confidence": probability,
        "detected": is_anomaly,
        "evidence": {
            "cpu_usage": float(row["CPU_Usage"]),
            "memory_usage": float(row["Memory_Usage"]),
            "disk_io": float(row["Disk_IO"]),
            "network_io": float(row["Network_IO"]),
            "hour": int(row["hour"]),
            "day": int(row["day"]),
            "day_of_week": int(row["day_of_week"]),
            "anomaly_probability": probability
        },
        "recommendation": {
            "root_cause": "AI model detected abnormal cloud resource behavior." if is_anomaly else "No abnormal cloud resource behavior detected.",
            "recommendation": "Investigate workload resource usage and possible cost impact." if is_anomaly else "No action required.",
            "estimated_daily_savings": 0,
            "automation_candidate": False,
            "requires_approval": True
        },
        "automation": {
            "can_automate": False,
            "risk_level": "medium" if is_anomaly else "low",
            "requires_approval": True
        }
    })

with open(OUTPUT_FILE, "w") as file:
    json.dump(results, file, indent=2)

print(f"Saved {len(results)} AI predictions to {OUTPUT_FILE}")