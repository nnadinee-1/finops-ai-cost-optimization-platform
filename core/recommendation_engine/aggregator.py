import json
import os


OUTPUT_FILE = "core/recommendation_engine/all_recommendations.json"

INPUT_FILES = [
    "cost-anomaly-alerting-pack/output/anomaly_results.json",
    "cost-anomaly-alerting-pack/ai/output/ai_predictions.json",
]


def load_json_file(file_path):
    if not os.path.exists(file_path):
        print(f"Skipping missing file: {file_path}")
        return []

    with open(file_path, "r") as file:
        data = json.load(file)

    if isinstance(data, list):
        return data

    return [data]


all_recommendations = []

for file_path in INPUT_FILES:
    all_recommendations.extend(load_json_file(file_path))

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, "w") as file:
    json.dump(all_recommendations, file, indent=2)

print(f"Aggregated {len(all_recommendations)} recommendations.")
print(f"Saved output to {OUTPUT_FILE}")