import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# -------------------------
# Load Data
# -------------------------
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "../data/processed/final.csv")

df = pd.read_csv(file_path)

# -------------------------
# Basic Cleaning
# -------------------------
# Drop useless columns
df.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1, inplace=True)

# Fill missing values
df["Age"].fillna(df["Age"].median(), inplace=True)
df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

# -------------------------
# Feature Engineering
# -------------------------
# Convert categorical to numeric
df["Sex"] = df["Sex"].map({"male": 1, "female": 0})

# One-hot encoding
df = pd.get_dummies(df, columns=["Embarked"], drop_first=True)

# -------------------------
# Split
# -------------------------
X = df.drop("Survived", axis=1)
y = df["Survived"]

# Save feature list
feature_list = X.columns.tolist()

# -------------------------
# Train Model
# -------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# -------------------------
# Save Model + Features
# -------------------------
model_path = os.path.join(current_dir, "../models/model.pkl")
feature_path = os.path.join(current_dir, "../models/feature_list.pkl")

with open(model_path, "wb") as f:
    pickle.dump(model, f)

with open(feature_path, "wb") as f:
    pickle.dump(feature_list, f)

print("✅ Training complete!")
print(f"Features used: {len(feature_list)}")