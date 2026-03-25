import pandas as pd

# Load original dataset (RAW, not processed)
train = pd.read_csv("src/data/raw/dataset.csv")

# Load prediction logs
logs = pd.read_csv("prediction_logs.csv")

# Only check common columns
common_cols = [col for col in logs.columns if col in train.columns]

drift_report = {}

for col in common_cols:
    if train[col].dtype in ["int64", "float64"]:
        train_mean = train[col].mean()
        log_mean = logs[col].mean()

        drift = abs(train_mean - log_mean)

        drift_report[col] = round(drift, 3)

print("Drift Report:")
print(drift_report)