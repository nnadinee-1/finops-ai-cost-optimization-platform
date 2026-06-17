import json
from collections import Counter

from detector import detect_cost_anomaly


DATA_FILE = "data/mock/infrastructure_metrics.json"

with open(DATA_FILE, "r") as file:
    records = json.load(file)


results = [detect_cost_anomaly(record) for record in records]

total_records = len(results)
detected_anomalies = [result for result in results if result["detected"]]
normal_records = [result for result in results if not result["detected"]]

severity_counts = Counter(result["severity"] for result in results)

print("Detection Summary Report")
print("------------------------")
print(f"Total records analyzed: {total_records}")
print(f"Detected anomalies: {len(detected_anomalies)}")
print(f"Normal records: {len(normal_records)}")
print(f"Detection rate: {(len(detected_anomalies) / total_records) * 100:.2f}%")

print("\nSeverity Distribution")
print("---------------------")
for severity in ["critical", "high", "medium", "low"]:
    print(f"{severity}: {severity_counts.get(severity, 0)}")

print("\nDetected Anomalies")
print("------------------")
for anomaly in detected_anomalies:
    print(f"Service: {anomaly['service']}")
    print(f"Namespace: {anomaly['namespace']}")
    print(f"Severity: {anomaly['severity']}")
    print(f"Daily cost: {anomaly['evidence']['daily_cost']}")
    print(f"Baseline: {anomaly['evidence']['avg_daily_cost_last_7_days']}")
    print(f"Increase: {anomaly['evidence']['increase_percentage']}%")
    print(f"Recommended action: {anomaly['recommendation']['action']}")
    print()