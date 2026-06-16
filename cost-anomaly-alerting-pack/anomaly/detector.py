def detect_cost_anomaly(service, historical_cost, current_cost):
    increase_percentage = ((current_cost - historical_cost) / historical_cost) * 100

    if increase_percentage >= 100:
        severity = "critical"
    elif increase_percentage >= 50:
        severity = "high"
    elif increase_percentage >= 30:
        severity = "medium"
    else:
        severity = "low"

    anomaly = current_cost > historical_cost * 1.5

    return {
        "service": service,
        "problem_type": "cost_anomaly",
        "historical_cost": historical_cost,
        "current_cost": current_cost,
        "increase_percentage": round(increase_percentage, 2),
        "anomaly": anomaly,
        "severity": severity,
        "recommendation": "Investigate CPU, memory, replicas, or traffic increase.",
        "action": "send_alert" if anomaly else "no_action"
    }


result = detect_cost_anomaly(
    service="backend-service",
    historical_cost=5,
    current_cost=18
)

print(result)