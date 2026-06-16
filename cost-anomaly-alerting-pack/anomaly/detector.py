import json


def detect_cost_anomaly(record):
    daily_cost = record["cost"]["daily_cost"]
    avg_cost = record["cost"]["avg_daily_cost_last_7_days"]

    increase_percentage = ((daily_cost - avg_cost) / avg_cost) * 100
    anomaly = daily_cost > avg_cost * 1.5

    if increase_percentage >= 100:
        severity = "critical"
    elif increase_percentage >= 50:
        severity = "high"
    elif increase_percentage >= 30:
        severity = "medium"
    else:
        severity = "low"

    return {
        "pack_name": "cost_anomaly_alerting",
        "service": record["workload"]["name"],
        "namespace": record["namespace"],
        "problem_type": "cost_anomaly",
        "severity": severity,
        "confidence": 0.9,
        "detected": anomaly,
        "evidence": {
            "daily_cost": daily_cost,
            "avg_daily_cost_last_7_days": avg_cost,
            "increase_percentage": round(increase_percentage, 2),
            "cost_drivers": record["cost_drivers"]
        },
        "recommendation": {
            "action": "investigate_cost_spike" if anomaly else "no_action",
            "current_value": f"${daily_cost}/day",
            "recommended_value": f"${avg_cost}/day baseline",
            "estimated_daily_savings": round(daily_cost - avg_cost, 2)
        },
        "explanation": "Daily cost is significantly higher than the 7-day average.",
        "automation": {
            "can_automate": anomaly,
            "risk_level": "medium" if anomaly else "low",
            "requires_approval": True
        }
    }


with open("cost-anomaly-alerting-pack/data/generated_cost_data.json", "r") as file:
    records = json.load(file)

for record in records:
    result = detect_cost_anomaly(record)
    print(json.dumps(result, indent=2))