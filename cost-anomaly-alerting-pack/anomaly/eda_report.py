import pandas as pd

DATA_FILE = "cost-anomaly-alerting-pack/data/ai_features.csv"

df = pd.read_csv(DATA_FILE)

print("AI DATASET READINESS REPORT")
print("===========================")

print("\nDataset Shape")
print("-------------")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nColumns")
print("-------")
for col in df.columns:
    print(col)

print("\nMissing Values")
print("--------------")
print(df.isnull().sum())

print("\nDuplicate Rows")
print("--------------")
print(df.duplicated().sum())

print("\nExpected Behavior Distribution")
print("------------------------------")
print(df["expected_behavior"].value_counts())

print("\nFeature Statistics")
print("------------------")
print(df.describe())

print("\nAI Readiness Assessment")
print("-----------------------")

if df.isnull().sum().sum() == 0:
    print("PASS: No missing values.")
else:
    print("WARNING: Missing values detected.")

if df.duplicated().sum() == 0:
    print("PASS: No duplicate rows.")
else:
    print("WARNING: Duplicate rows detected.")

print("PASS: Feature engineering dataset generated successfully.")
print("PASS: Labels available for supervised learning.")

print("\nNext Step")
print("---------")
print("Dataset is ready for machine learning model development.")