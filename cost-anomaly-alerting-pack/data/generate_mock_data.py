import json
import random
from datetime import datetime, timedelta


SERVICES = [
    "backend-service",
    "frontend-service",
    "payment-service",
    "worker-service",
    "cache-service"
]


def generate_record(service, day_index):
    base_cost = {
        "backend-service": 6,
        "frontend-service": 3,
        "payment-service": 8,
        "worker-service": 5,
        "cache-service": 4
    }[service]

    daily_cost = round(base_cost + random.uniform(-1, 1), 2)

    # Inject realistic anomaly
    if service == "backend-service" and day_index == 20:
        daily_cost = round(base_cost * 3.5, 2)

    cpu_cost = round(daily_cost * random.uniform(0.25, 0.35), 2)
    memory_cost = round(daily_cost * random.uniform(0.20, 0.30), 2)
    replica_cost = round(daily_cost * random.uniform(0.25, 0.40), 2)
    storage_cost = round(daily_cost - cpu_cost - memory_cost - replica_cost, 2)

    return {
        "timestamp": (datetime(2026, 6, 1) + timedelta(days=day_index)).isoformat() + "Z",
        "cluster_id": "dev-cluster-01",
        "namespace": "production",
        "workload": {
            "name": service,
            "type": "deployment",
            "replicas": random.choice([2, 3, 4, 5])
        },
        "cost": {
            "daily_cost": daily_cost,
            "avg_daily_cost_last_7_days": base_cost
        },
        "cost_drivers": {
            "cpu_cost": cpu_cost,
            "memory_cost": memory_cost,
            "replica_cost": replica_cost,
            "storage_cost": storage_cost
        },
        "expected_behavior": "critical_anomaly"
        if service == "backend-service" and day_index == 20
        else "normal"
    }


records = []

for day in range(30):
    for service in SERVICES:
        records.append(generate_record(service, day))


with open("cost-anomaly-alerting-pack/data/generated_cost_data.json", "w") as file:
    json.dump(records, file, indent=2)

print("Generated 150 cost records successfully.")