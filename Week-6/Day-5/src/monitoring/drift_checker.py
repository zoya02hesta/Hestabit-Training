import pandas as pd

# Load datasets
train = pd.read_csv("src/data/raw/dataset.csv")
logs = pd.read_csv("prediction_logs.csv")

# Common columns
common_cols = [col for col in logs.columns if col in train.columns]

drift_report = {}

print("\n🔍 Drift Analysis Report\n")

for col in common_cols:
    if train[col].dtype in ["int64", "float64"]:
        train_mean = train[col].mean()
        log_mean = logs[col].mean()

        drift = abs(train_mean - log_mean)

        drift_report[col] = round(drift, 4)

        print(f"{col}: Drift = {drift:.4f}")

        if drift > 0.1:
            print(f"⚠️ Significant drift detected in {col}\n")

print("\n✅ Drift check completed")