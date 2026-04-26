import pandas as pd
import numpy as np
import os
import pickle
import json

from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

# XGBoost (install if not installed)
from xgboost import XGBClassifier

# -------------------------
# Paths
# -------------------------
current_dir = os.path.dirname(__file__)

data_path = os.path.join(current_dir, "../data/processed/final.csv")
model_path = os.path.join(current_dir, "../models/best_model.pkl")
feature_path = os.path.join(current_dir, "../models/feature_list.pkl")
metrics_path = os.path.join(current_dir, "../evaluation/metrics.json")

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv(data_path)

# -------------------------
# Cleaning
# -------------------------
df.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1, inplace=True)

df["Age"].fillna(df["Age"].median(), inplace=True)
df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

# -------------------------
# Feature Engineering
# -------------------------
df["Sex"] = df["Sex"].map({"male": 1, "female": 0})
df = pd.get_dummies(df, columns=["Embarked"], drop_first=True)

# -------------------------
# Split
# -------------------------
X = df.drop("Survived", axis=1)
y = df["Survived"]

feature_list = X.columns.tolist()

# -------------------------
# Models (REQUIRED 4)
# -------------------------
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "RandomForest": RandomForestClassifier(random_state=42),
    "XGBoost": XGBClassifier(eval_metric="logloss"),
    "NeuralNetwork": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500)
}

# -------------------------
# Metrics
# -------------------------
scoring = {
    "accuracy": make_scorer(accuracy_score),
    "precision": make_scorer(precision_score),
    "recall": make_scorer(recall_score),
    "f1": make_scorer(f1_score),
    "roc_auc": make_scorer(roc_auc_score)
}

results = {}

best_model = None
best_score = 0
best_model_name = ""

# -------------------------
# Training + CV
# -------------------------
for name, model in models.items():
    print(f"\nTraining {name}...")

    cv_results = cross_validate(
        model,
        X,
        y,
        cv=5,
        scoring=scoring,
        return_train_score=False
    )

    # Average scores
    metrics = {
        "accuracy": np.mean(cv_results["test_accuracy"]),
        "precision": np.mean(cv_results["test_precision"]),
        "recall": np.mean(cv_results["test_recall"]),
        "f1": np.mean(cv_results["test_f1"]),
        "roc_auc": np.mean(cv_results["test_roc_auc"])
    }

    results[name] = metrics

    print(f"{name} ROC-AUC: {metrics['roc_auc']:.4f}")

    # Select best model using ROC-AUC
    if metrics["roc_auc"] > best_score:
        best_score = metrics["roc_auc"]
        best_model = model
        best_model_name = name

# -------------------------
# Train Best Model on Full Data
# -------------------------
best_model.fit(X, y)

# -------------------------
# Confusion Matrix (DAY-3 REQUIREMENT)
# -------------------------
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

y_pred = best_model.predict(X)

cm = confusion_matrix(y, y_pred)

plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt="d")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

cm_path = os.path.join(current_dir, "../evaluation/confusion_matrix.png")
plt.savefig(cm_path)

print("✅ Confusion matrix saved!")

print("\n✅ Best Model:", best_model_name)
print("✅ Best ROC-AUC:", best_score)

# -------------------------
# Save Files
# -------------------------
with open(model_path, "wb") as f:
    pickle.dump(best_model, f)

with open(feature_path, "wb") as f:
    pickle.dump(feature_list, f)

with open(metrics_path, "w") as f:
    json.dump(results, f, indent=4)

print("\n✅ Model, features, and metrics saved!")