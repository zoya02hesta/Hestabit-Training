import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

from src.features.build_features import run_feature_pipeline


def train_models():

    X_train, X_test, y_train, y_test = run_feature_pipeline()

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(),
        "XGBoost": XGBClassifier(eval_metric="logloss"),
        "NeuralNetwork": MLPClassifier(max_iter=500)
    }

    results = {}
    best_model = None
    best_score = 0
    best_model_name = None

    for name, model in models.items():

        print(f"Training {name}")

        scores = cross_validate(
            model,
            X_train,
            y_train,
            cv=5,
            scoring=["accuracy", "precision", "recall", "f1", "roc_auc"]
        )

        metrics = {
            "accuracy": scores["test_accuracy"].mean(),
            "precision": scores["test_precision"].mean(),
            "recall": scores["test_recall"].mean(),
            "f1": scores["test_f1"].mean(),
            "roc_auc": scores["test_roc_auc"].mean()
        }

        results[name] = metrics

        if metrics["roc_auc"] > best_score:
            best_score = metrics["roc_auc"]
            best_model = model
            best_model_name = name

    print(f"Best model: {best_model_name}")

    best_model.fit(X_train, y_train)

    y_pred = best_model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Confusion Matrix")
    plt.savefig("src/evaluation/confusion_matrix.png")

    joblib.dump(best_model, "src/models/best_model.pkl")

    with open("src/evaluation/metrics.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Best model saved")
    print("Metrics saved")


if __name__ == "__main__":
    train_models()