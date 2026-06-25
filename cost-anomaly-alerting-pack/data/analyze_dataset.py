import json


DATA_FILE = "cost-anomaly-alerting-pack/data/generated_cost_data.json"


with open(DATA_FILE, "r") as file:
    records = json.load(file)


total_records = len(records)
services = sorted(set(record["workload"]["name"] for record in records))

normal_records = [
    record for record in records
    if record["expected_behavior"] == "normal"
]

anomaly_records = [
    record for record in records
    if record["expected_behavior"] != "normal"
]

daily_costs = [record["cost"]["daily_cost"] for record in records]

highest_record = max(records, key=lambda record: record["cost"]["daily_cost"])
lowest_record = min(records, key=lambda record: record["cost"]["daily_cost"])

average_daily_cost = sum(daily_costs) / total_records


print("Dataset Summary")
print("----------------")
print(f"Total records: {total_records}")
print(f"Services count: {len(services)}")
print(f"Services: {services}")
print(f"Normal records: {len(normal_records)}")
print(f"Anomaly records: {len(anomaly_records)}")
print(f"Average daily cost: ${average_daily_cost:.2f}")
print(f"Highest daily cost: ${highest_record['cost']['daily_cost']} - {highest_record['workload']['name']} - {highest_record['timestamp']}")
print(f"Lowest daily cost: ${lowest_record['cost']['daily_cost']} - {lowest_record['workload']['name']} - {lowest_record['timestamp']}")

print("\nAnomaly Details")
print("----------------")
for record in anomaly_records:
    print(f"Service: {record['workload']['name']}")
    print(f"Timestamp: {record['timestamp']}")
    print(f"Daily cost: ${record['cost']['daily_cost']}")
    print(f"Baseline: ${record['cost']['avg_daily_cost_last_7_days']}")
    print(f"Expected behavior: {record['expected_behavior']}")