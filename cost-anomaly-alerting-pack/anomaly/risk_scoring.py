def calculate_risk_score(record):
    score = 0
    reasons = []

    daily_cost = record["cost"]["daily_cost"]
    baseline = record["history"]["avg_daily_cost_last_7_days"]
    increase_percentage = ((daily_cost - baseline) / baseline) * 100

    usage = record["resource_usage"]

    cpu_request = usage["cpu_request_millicores"]
    cpu_usage = usage["cpu_usage_millicores"]
    memory_request = usage["memory_request_mb"]
    memory_usage = usage["memory_usage_mb"]
    replicas = record["workload"]["replicas"]
    traffic = usage["traffic_requests_per_minute"]
    storage_gb = usage["storage_gb"]
    logs_gb = usage["log_volume_gb_per_day"]

    cpu_utilization = (cpu_usage / cpu_request) * 100
    memory_utilization = (memory_usage / memory_request) * 100

    # Cost behavior
    if increase_percentage >= 20:
        score += 2
        reasons.append("Cost increased by at least 20% compared to baseline")

    if increase_percentage >= 50:
        score += 3
        reasons.append("Cost increased by at least 50% compared to baseline")

    if increase_percentage >= 100:
        score += 4
        reasons.append("Cost more than doubled compared to baseline")

    # Resource pressure
    if cpu_utilization >= 90:
        score += 3
        reasons.append("CPU utilization is very high")

    if memory_utilization >= 90:
        score += 3
        reasons.append("Memory utilization is very high")

    # Scaling behavior
    if replicas >= 7:
        score += 3
        reasons.append("Replica count is unusually high")

    # Inefficient cost behavior
    if traffic < 50 and daily_cost > baseline:
        score += 4
        reasons.append("Cost increased while traffic is very low")

    # Storage and logs
    if storage_gb >= 500:
        score += 4
        reasons.append("Storage usage is abnormally high")

    if logs_gb >= 80:
        score += 4
        reasons.append("Log volume is abnormally high")

    # Idle resources
    if cpu_utilization < 10 and memory_utilization < 15 and traffic == 0 and replicas >= 3:
        score += 5
        reasons.append("Workload appears idle while still running multiple replicas")

    return {
        "risk_score": score,
        "reasons": reasons,
        "increase_percentage": round(increase_percentage, 2),
        "cpu_utilization": round(cpu_utilization, 2),
        "memory_utilization": round(memory_utilization, 2)
    }


def severity_from_score(score):
    if score >= 12:
        return "critical"
    elif score >= 9:
        return "high"
    elif score >= 6:
        return "medium"
    elif score >= 3:
        return "low"
    return "normal"