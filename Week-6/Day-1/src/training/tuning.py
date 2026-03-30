import json
import os
import optuna
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from src.features.build_features import run_feature_pipeline


# -------------------------
# Load Data ONCE
# -------------------------
X_train, X_test, y_train, y_test = run_feature_pipeline()


# -------------------------
# Optuna Objective
# -------------------------
def objective(trial):

    params = {
        "C": trial.suggest_float("C", 0.01, 10),
        "penalty": trial.suggest_categorical("penalty", ["l1", "l2"]),
        "solver": "liblinear"
    }

    model = LogisticRegression(**params)

    score = cross_val_score(
        model,
        X_train,
        y_train,
        cv=5,
        scoring="roc_auc"
    ).mean()

    return score


# -------------------------
# Run Tuning
# -------------------------
def run_tuning():

    os.makedirs("src/models", exist_ok=True)
    os.makedirs("src/tuning", exist_ok=True)
    os.makedirs("src/evaluation", exist_ok=True)

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=20)

    best_params = study.best_params
    best_score = study.best_value

    print("Best Params:", best_params)
    print("Best CV ROC-AUC:", best_score)

    # -------------------------
    # Train Final Model
    # -------------------------
    best_model = LogisticRegression(**best_params, solver="liblinear")
    best_model.fit(X_train, y_train)

    # -------------------------
    # Evaluation
    # -------------------------
    y_pred = best_model.predict(X_test)
    y_proba = best_model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba)
    }

    print("\nFinal Test Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")

    # -------------------------
    # Save Model
    # -------------------------
    joblib.dump(best_model, "src/models/best_model_tuned.pkl")

    # -------------------------
    # Save Results
    # -------------------------
    results = {
        "best_params": best_params,
        "cv_best_score": best_score,
        "test_metrics": metrics
    }

    with open("src/tuning/results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("\n✅ Tuned model saved")
    print("✅ Results saved")

    # -------------------------
    # Feature Importance (COEFFICIENTS)
    # -------------------------
    importance = best_model.coef_[0]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=importance, y=range(len(importance)))
    plt.title("Feature Importance (Logistic Coefficients)")
    plt.tight_layout()
    plt.savefig("src/evaluation/feature_importance_model.png")

    print("✅ Feature importance saved")

    # -------------------------
    # Confusion Matrix
    # -------------------------
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Error Analysis Heatmap")
    plt.tight_layout()
    plt.savefig("src/evaluation/error_heatmap.png")

    print("✅ Error heatmap saved")


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    run_tuning()