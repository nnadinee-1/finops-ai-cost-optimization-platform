import json
from risk_scoring import calculate_risk_score, severity_from_score
from recommendation_engine import build_recommendation

DATA_FILE = "data/mock/infrastructure_metrics.json"
OUTPUT_FILE = "cost-anomaly-alerting-pack/output/anomaly_results.json"


def build_explanation(anomaly, increase_percentage):
    if anomaly:
        return (
            f"Risk score indicates a potential cost anomaly. "
            f"Cost changed by {round(increase_percentage, 2)}% compared to baseline."
        )

    return "Risk score is within the expected range."


def detect_cost_anomaly(record):
    
    daily_cost = record["cost"]["daily_cost"]
    avg_cost = record["history"]["avg_daily_cost_last_7_days"]

    risk = calculate_risk_score(record)

    increase_percentage = risk["increase_percentage"]
    severity = severity_from_score(risk["risk_score"])
    anomaly = severity in ["medium", "high", "critical"] and increase_percentage >= 20

    recommendation = build_recommendation(
        "cost_anomaly" if anomaly else "normal",
        risk
    )
    
    return {
        "pack_name": "cost_anomaly_alerting",
        "service": record["workload"]["name"],
        "namespace": record["namespace"],
        "problem_type": "cost_anomaly",
        "severity": severity,
        "confidence": 0.9 if anomaly else 0.75,
        "detected": anomaly,
        "evidence": {
            "timestamp": record["timestamp"],
            "daily_cost": daily_cost,
            "avg_daily_cost_last_7_days": avg_cost,
            "increase_percentage": round(increase_percentage, 2),
            "risk_score": risk["risk_score"],
            "risk_reasons": risk["reasons"],
            "cpu_utilization": risk["cpu_utilization"],
            "memory_utilization": risk["memory_utilization"],
            "resource_usage": record["resource_usage"],
            "expected_behavior": record["expected_behavior"]
        },
        "recommendation": recommendation,
        "explanation": build_explanation(anomaly, increase_percentage),
        "automation": {
            "can_automate": False,
            "risk_level": "medium" if anomaly else "low",
            "requires_approval": True
        }
    }


if __name__ == "__main__":
    with open(DATA_FILE, "r") as file:
        records = json.load(file)

    results = [detect_cost_anomaly(record) for record in records]

    with open(OUTPUT_FILE, "w") as file:
        json.dump(results, file, indent=2)

    print(f"Saved {len(results)} anomaly detection results to {OUTPUT_FILE}")