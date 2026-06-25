import json

RESULTS_FILE = "cost-anomaly-alerting-pack/output/anomaly_results.json"

with open(RESULTS_FILE, "r") as file:
    results = json.load(file)

print("=" * 60)
print("ENTERPRISE FINOPS AI COST OPTIMIZATION REPORT")
print("=" * 60)

risk_cases = [
    r for r in results
    if r["severity"] in ["low", "medium", "high", "critical"]
]

print(f"\nTotal services analyzed: {len(results)}")
print(f"Potential optimization cases: {len(risk_cases)}")

for case in risk_cases:

    print("\n" + "=" * 60)

    print(f"Service: {case['service']}")
    print(f"Namespace: {case['namespace']}")

    print(f"\nSeverity: {case['severity'].upper()}")

    print("\nProblem:")
    print(case["explanation"])

    print("\nRecommendation:")
    print(case["recommendation"]["recommendation"])

    print("\nEstimated Daily Savings:")
    print(f"${case['recommendation']['estimated_daily_savings']}")

    print("\nAutomation:")

    if case["automation"]["can_automate"]:
        print("Can be automated with approval.")
    else:
        print("Manual review recommended.")

print("\n" + "=" * 60)
print("Report generation completed.")
print("=" * 60)