import json
import optuna
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix

from src.features.build_features import run_feature_pipeline


def objective(trial):

    X_train, X_test, y_train, y_test = run_feature_pipeline()

    params = {
    "n_estimators": trial.suggest_int("n_estimators", 150, 400),
    "max_depth": trial.suggest_int("max_depth", 6, 25),
    "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
}

    model = RandomForestClassifier(**params)

    score = cross_val_score(
        model,
        X_train,
        y_train,
        cv=5,
        scoring="roc_auc"
    ).mean()

    return score


def run_tuning():

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=20)

    best_params = study.best_params
    best_score = study.best_value

    print("Best Params:", best_params)
    print("Best ROC-AUC:", best_score)

    # Train final model
    X_train, X_test, y_train, y_test = run_feature_pipeline()

    best_model = RandomForestClassifier(
    **best_params,
    class_weight={0: 1, 1: 3}
)
    best_model.fit(X_train, y_train)

    # Save model
    joblib.dump(best_model, "src/models/best_model_tuned.pkl")

    # Save tuning results
    results = {
        "best_params": best_params,
        "best_score": best_score
    }

    with open("src/tuning/results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Tuned model saved")
    print("Results saved")

    # ==============================
    # FEATURE IMPORTANCE
    # ==============================
    importances = best_model.feature_importances_

    plt.figure(figsize=(10,5))
    plt.bar(range(len(importances)), importances)
    plt.title("Feature Importance")
    plt.savefig("src/evaluation/feature_importance_model.png")

    print("Feature importance plot saved")

    # ==============================
    # ERROR ANALYSIS (CONFUSION MATRIX)
    # ==============================
    y_pred = best_model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Error Analysis Heatmap")
    plt.savefig("src/evaluation/error_heatmap.png")

    print("Error heatmap saved")


if __name__ == "__main__":
    run_tuning()