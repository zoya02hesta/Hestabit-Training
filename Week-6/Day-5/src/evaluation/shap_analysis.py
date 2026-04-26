import shap
import joblib
import matplotlib.pyplot as plt
import numpy as np
import os

from src.features.build_features import run_feature_pipeline


def run_shap_analysis():

    os.makedirs("src/evaluation", exist_ok=True)

    # Load data
    X_train, X_test, y_train, y_test = run_feature_pipeline()

    # Load model
    model = joblib.load("src/models/best_model_tuned.pkl")

    print("✅ Model loaded")

    # Use LinearExplainer for Logistic Regression
    explainer = shap.LinearExplainer(model, X_train)
    shap_values = explainer.shap_values(X_test)

    # -------------------------
    # SHAP Summary Plot
    # -------------------------
    shap.summary_plot(shap_values, X_test, show=False)
    plt.savefig("src/evaluation/shap_summary.png")
    plt.close()

    print("✅ SHAP summary plot saved")

    # -------------------------
    # SHAP Importance
    # -------------------------
    shap_importance = np.abs(shap_values).mean(axis=0)

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(shap_importance)), shap_importance)
    plt.title("SHAP Feature Importance")
    plt.tight_layout()
    plt.savefig("src/evaluation/shap_importance.png")

    print("✅ SHAP feature importance saved")


if __name__ == "__main__":
    run_shap_analysis()