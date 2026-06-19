import json
import csv

from risk_scoring import calculate_risk_score


DATA_FILE = "data/mock/infrastructure_metrics.json"
OUTPUT_FILE = "cost-anomaly-alerting-pack/data/ai_features.csv"


def extract_features(record):
    usage = record["resource_usage"]

    cpu_request = usage["cpu_request_millicores"]
    cpu_usage = usage["cpu_usage_millicores"]

    memory_request = usage["memory_request_mb"]
    memory_usage = usage["memory_usage_mb"]

    daily_cost = record["cost"]["daily_cost"]
    baseline_cost = record["history"]["avg_daily_cost_last_7_days"]

    cpu_utilization = (cpu_usage / cpu_request) * 100
    memory_utilization = (memory_usage / memory_request) * 100
    cost_increase_percentage = ((daily_cost - baseline_cost) / baseline_cost) * 100

    risk = calculate_risk_score(record)

    idle_indicator = (
        cpu_utilization < 10
        and memory_utilization < 15
        and usage["traffic_requests_per_minute"] == 0
    )

    return {
        "timestamp": record["timestamp"],
        "service": record["workload"]["name"],
        "namespace": record["namespace"],
        "cpu_utilization": round(cpu_utilization, 2),
        "memory_utilization": round(memory_utilization, 2),
        "cost_increase_percentage": round(cost_increase_percentage, 2),
        "replicas": record["workload"]["replicas"],
        "traffic_requests_per_minute": usage["traffic_requests_per_minute"],
        "storage_gb": usage["storage_gb"],
        "log_volume_gb_per_day": usage["log_volume_gb_per_day"],
        "idle_indicator": int(idle_indicator),
        "risk_score": risk["risk_score"],
        "expected_behavior": record["expected_behavior"]
    }


with open(DATA_FILE, "r") as file:
    records = json.load(file)

features = [extract_features(record) for record in records]

with open(OUTPUT_FILE, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=features[0].keys())
    writer.writeheader()
    writer.writerows(features)

print(f"Saved {len(features)} AI feature rows to {OUTPUT_FILE}")