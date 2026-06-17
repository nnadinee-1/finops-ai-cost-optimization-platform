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

ANOMALY_SCENARIOS = {
    ("backend-service", 40): "cpu_spike",
    ("payment-service", 75): "memory_spike",
    ("logging-service", 100): "log_growth",
    ("ml-inference-service", 130): "cost_spike",
    ("database-service", 160): "storage_growth",
    ("worker-service", 95): "idle_resource"
}


def calculate_cost(cpu_request, memory_request, replicas, storage_gb, log_gb):
    cpu_cost = (cpu_request / 1000) * 0.04 * 24 * replicas
    memory_cost = (memory_request / 1024) * 0.005 * 24 * replicas
    storage_cost = storage_gb * 0.02
    log_cost = log_gb * 0.01
    return round(cpu_cost + memory_cost + storage_cost + log_cost, 2)


def generate_record(service, day_index):
    timestamp = (datetime(2026, 1, 1) + timedelta(days=day_index)).isoformat() + "Z"

    cpu_request = random.choice([500, 750, 1000, 1500])
    cpu_usage = int(cpu_request * random.uniform(0.25, 0.75))

    memory_request = random.choice([512, 1024, 2048, 4096])
    memory_usage = int(memory_request * random.uniform(0.25, 0.75))

    replicas = random.choice([2, 3, 4])
    traffic = random.randint(80, 900)

    storage_gb = round(random.uniform(20, 150), 2)
    log_gb = round(random.uniform(1, 15), 2)

    scenario = ANOMALY_SCENARIOS.get((service, day_index), "normal")

    if scenario == "cpu_spike":
        cpu_usage = int(cpu_request * random.uniform(1.2, 1.6))
        replicas = random.choice([6, 8, 10])
        traffic = random.randint(1500, 3000)

    elif scenario == "memory_spike":
        memory_usage = int(memory_request * random.uniform(1.1, 1.5))
        replicas = random.choice([5, 6, 7])

    elif scenario == "log_growth":
        log_gb = round(random.uniform(80, 150), 2)

    elif scenario == "storage_growth":
        storage_gb = round(random.uniform(500, 900), 2)

    elif scenario == "idle_resource":
        cpu_usage = int(cpu_request * random.uniform(0.01, 0.05))
        memory_usage = int(memory_request * random.uniform(0.05, 0.10))
        traffic = 0
        replicas = random.choice([3, 4, 5])

    elif scenario == "cost_spike":
        cpu_request = 3000
        memory_request = 8192
        replicas = 10
        cpu_usage = int(cpu_request * random.uniform(0.8, 1.2))
        memory_usage = int(memory_request * random.uniform(0.7, 1.1))
        traffic = random.randint(2000, 4000)

    daily_cost = calculate_cost(cpu_request, memory_request, replicas, storage_gb, log_gb)

    return {
        "timestamp": timestamp,
        "cluster_id": "dev-cluster-01",
        "namespace": random.choice(["production", "staging"]),
        "workload": {
            "name": service,
            "type": "deployment",
            "replicas": replicas
        },
        "resource_usage": {
            "cpu_request_millicores": cpu_request,
            "cpu_usage_millicores": cpu_usage,
            "memory_request_mb": memory_request,
            "memory_usage_mb": memory_usage,
            "storage_gb": storage_gb,
            "log_volume_gb_per_day": log_gb,
            "traffic_requests_per_minute": traffic
        },
        "cost": {
            "daily_cost": daily_cost,
            "monthly_estimate": round(daily_cost * 30, 2)
        },
        "history": {
            "avg_daily_cost_last_7_days": round(
                daily_cost * random.uniform(0.75, 1.05), 2
            )
        },
        "metadata": {
            "owner_team": random.choice(
                ["backend-team", "platform-team", "data-team"]
            ),
            "environment": "production",
            "criticality": random.choice(
                ["low", "medium", "high"]
            )
        },
        "expected_behavior": scenario
    }


records = []

for day in range(180):
    for service in SERVICES:
        records.append(generate_record(service, day))


with open("data/mock/infrastructure_metrics.json", "w") as file:
    json.dump(records, file, indent=2)

print(f"Generated {len(records)} shared infrastructure records.")