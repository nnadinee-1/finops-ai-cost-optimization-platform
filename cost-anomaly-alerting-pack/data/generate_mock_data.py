import json
import random
from datetime import datetime, timedelta


random.seed(42)

SERVICES = [
    "backend-service",
    "frontend-service",
    "payment-service",
    "worker-service",
    "cache-service",
    "auth-service",
    "notification-service",
    "reporting-service",
    "search-service",
    "billing-service",
    "analytics-service",
    "inventory-service",
    "order-service",
    "recommendation-service",
    "email-service",
    "logging-service",
    "gateway-service",
    "database-service",
    "queue-service",
    "ml-inference-service"
]

BASE_COST = {
    service: random.randint(3, 15)
    for service in SERVICES
}


ANOMALY_DAYS = {
    ("backend-service", 40): "critical_anomaly",
    ("payment-service", 75): "high_anomaly",
    ("logging-service", 100): "medium_anomaly",
    ("ml-inference-service", 130): "critical_anomaly",
    ("database-service", 160): "high_anomaly"
}


def get_seasonal_multiplier(day_index):
    # Weekends usually have slightly lower usage
    day_of_week = day_index % 7
    if day_of_week in [5, 6]:
        return 0.85

    # Monthly peak around billing/reporting days
    if day_index % 30 in [0, 1, 2]:
        return 1.25

    return 1.0


def get_anomaly_multiplier(anomaly_type):
    if anomaly_type == "medium_anomaly":
        return 1.4
    if anomaly_type == "high_anomaly":
        return 1.9
    if anomaly_type == "critical_anomaly":
        return 3.5
    return 1.0


def split_cost_drivers(daily_cost, anomaly_type):
    if anomaly_type == "critical_anomaly":
        cpu_weight = random.uniform(0.35, 0.45)
        memory_weight = random.uniform(0.20, 0.30)
        replica_weight = random.uniform(0.20, 0.30)
    elif anomaly_type == "high_anomaly":
        cpu_weight = random.uniform(0.25, 0.35)
        memory_weight = random.uniform(0.25, 0.35)
        replica_weight = random.uniform(0.20, 0.30)
    elif anomaly_type == "medium_anomaly":
        cpu_weight = random.uniform(0.20, 0.30)
        memory_weight = random.uniform(0.20, 0.30)
        replica_weight = random.uniform(0.25, 0.35)
    else:
        cpu_weight = random.uniform(0.25, 0.35)
        memory_weight = random.uniform(0.20, 0.30)
        replica_weight = random.uniform(0.25, 0.35)

    cpu_cost = round(daily_cost * cpu_weight, 2)
    memory_cost = round(daily_cost * memory_weight, 2)
    replica_cost = round(daily_cost * replica_weight, 2)
    storage_cost = round(max(daily_cost - cpu_cost - memory_cost - replica_cost, 0), 2)

    return {
        "cpu_cost": cpu_cost,
        "memory_cost": memory_cost,
        "replica_cost": replica_cost,
        "storage_cost": storage_cost
    }


def generate_record(service, day_index):
    base_cost = BASE_COST[service]
    timestamp = (datetime(2026, 1, 1) + timedelta(days=day_index)).isoformat() + "Z"

    anomaly_type = ANOMALY_DAYS.get((service, day_index), "normal")

    noise = random.uniform(-0.15, 0.15)
    seasonal_multiplier = get_seasonal_multiplier(day_index)
    anomaly_multiplier = get_anomaly_multiplier(anomaly_type)

    daily_cost = round(
        base_cost * seasonal_multiplier * anomaly_multiplier * (1 + noise),
        2
    )

    replicas = random.choice([2, 3, 4, 5])
    if anomaly_type in ["high_anomaly", "critical_anomaly"]:
        replicas = random.choice([7, 8, 9, 10])

    return {
        "timestamp": timestamp,
        "cluster_id": "dev-cluster-01",
        "namespace": random.choice(["production", "staging"]),
        "workload": {
            "name": service,
            "type": "deployment",
            "replicas": replicas
        },
        "cost": {
            "daily_cost": daily_cost,
            "avg_daily_cost_last_7_days": base_cost
        },
        "cost_drivers": split_cost_drivers(daily_cost, anomaly_type),
        "expected_behavior": anomaly_type
    }


records = []

DAYS = 180

for day in range(DAYS):
    for service in SERVICES:
        records.append(generate_record(service, day))


with open("cost-anomaly-alerting-pack/data/generated_cost_data.json", "w") as file:
    json.dump(records, file, indent=2)

print(f"Generated {len(records)} cost records successfully.")