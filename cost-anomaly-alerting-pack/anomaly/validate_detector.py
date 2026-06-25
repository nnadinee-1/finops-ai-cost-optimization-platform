import json

RESULTS_FILE = "cost-anomaly-alerting-pack/output/anomaly_results.json"
DATA_FILE = "data/mock/infrastructure_metrics.json"

with open(RESULTS_FILE, "r") as f:
    results = json.load(f)

with open(DATA_FILE, "r") as f:
    records = json.load(f)

print(f"Total infrastructure records: {len(records)}")
print(f"Total detector results: {len(results)}")
expected_anomalies = [
    record for record in records
    if record["expected_behavior"] != "normal"
]

detected_anomalies = [
    result for result in results
    if result["detected"] is True
]

print(f"Expected anomalies: {len(expected_anomalies)}")
print(f"Detected anomalies: {len(detected_anomalies)}")
expected_anomaly_keys = {
    (record["timestamp"], record["workload"]["name"])
    for record in expected_anomalies
}

detected_anomaly_keys = {
    (result["evidence"].get("timestamp"), result["service"])
    for result in detected_anomalies
}

correct_detections = expected_anomaly_keys & detected_anomaly_keys
false_positives = detected_anomaly_keys - expected_anomaly_keys
false_negatives = expected_anomaly_keys - detected_anomaly_keys

print(f"Correct detections: {len(correct_detections)}")
print(f"False positives: {len(false_positives)}")
print(f"False negatives: {len(false_negatives)}")
