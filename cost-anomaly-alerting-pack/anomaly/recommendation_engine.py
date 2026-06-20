def build_recommendation(problem_type, evidence):
    recommendation = {
        "root_cause": "Unknown",
        "recommendation": "Manual investigation required.",
        "estimated_daily_savings": 0,
        "automation_candidate": False,
        "requires_approval": True
    }

    if problem_type == "idle_resources":
        recommendation.update({
            "root_cause": "Resources are allocated but workload is idle.",
            "recommendation": "Scale down idle replicas.",
            "estimated_daily_savings": 3,
            "automation_candidate": True
        })

    elif problem_type == "high_cpu":
        recommendation.update({
            "root_cause": "CPU utilization is consistently high.",
            "recommendation": "Tune CPU requests or enable autoscaling.",
            "estimated_daily_savings": 4,
            "automation_candidate": True
        })

    elif problem_type == "high_memory":
        recommendation.update({
            "root_cause": "Memory allocation is inefficient.",
            "recommendation": "Optimize memory requests and limits.",
            "estimated_daily_savings": 4,
            "automation_candidate": True
        })

    elif problem_type == "high_storage":
        recommendation.update({
            "root_cause": "Storage consumption is excessive.",
            "recommendation": "Archive or clean unused storage.",
            "estimated_daily_savings": 5,
            "automation_candidate": False
        })

    elif problem_type == "high_logs":
        recommendation.update({
            "root_cause": "Log generation is unusually high.",
            "recommendation": "Enable log rotation and reduce retention.",
            "estimated_daily_savings": 2,
            "automation_candidate": True
        })

    elif problem_type == "cost_anomaly":
        recommendation.update({
            "root_cause": "Unexpected cost increase detected.",
            "recommendation": "Investigate cost drivers and optimize resources.",
            "estimated_daily_savings": 5,
            "automation_candidate": False
        })
    
    elif problem_type == "normal":
        recommendation.update({
            "root_cause": "No cost or infrastructure risk detected.",
            "recommendation": "No action required.",
            "estimated_daily_savings": 0,
            "automation_candidate": False
        })
    return recommendation