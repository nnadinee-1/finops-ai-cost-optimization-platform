import json


DATA_FILE = "cost-anomaly-alerting-pack/data/generated_cost_data.json"


def calculate_severity(increase_percentage):
    if increase_percentage >= 100:
        return "critical"
    elif increase_percentage >= 50:
        return "high"
    elif increase_percentage >= 30:
        return "medium"
    else:
        return "low"


def is_anomaly(severity):
    return severity in ["medium", "high", "critical"]


def build_explanation(anomaly, increase_percentage):
    if anomaly:
        return (
            f"Daily cost increased by {round(increase_percentage, 2)}% "
            "compared to the 7-day average, which indicates a cost anomaly."
        )

    return "Daily cost is within the expected range compared to the 7-day average."


def detect_cost_anomaly(record):
    daily_cost = record["cost"]["daily_cost"]
    avg_cost = record["cost"]["avg_daily_cost_last_7_days"]

    increase_percentage = ((daily_cost - avg_cost) / avg_cost) * 100

    severity = calculate_severity(increase_percentage)
    anomaly = is_anomaly(severity)

    return {
        "pack_name": "cost_anomaly_alerting",
        "service": record["workload"]["name"],
        "namespace": record["namespace"],
        "problem_type": "cost_anomaly",
        "severity": severity,
        "confidence": 0.9 if anomaly else 0.75,
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
            "estimated_daily_savings": round(max(daily_cost - avg_cost, 0), 2)
        },
        "explanation": build_explanation(anomaly, increase_percentage),
        "automation": {
            "can_automate": anomaly,
            "risk_level": "medium" if anomaly else "low",
            "requires_approval": True
        }
    }


if __name__ == "__main__":
    with open(DATA_FILE, "r") as file:
        records = json.load(file)

    results = [detect_cost_anomaly(record) for record in records]

    output_file = "cost-anomaly-alerting-pack/output/anomaly_results.json"

    with open(output_file, "w") as file:
        json.dump(results, file, indent=2)

    print(f"Saved {len(results)} anomaly detection results to {output_file}")