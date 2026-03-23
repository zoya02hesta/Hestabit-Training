import shap
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix
from src.features.build_features import run_feature_pipeline


def run_shap():

    # Load data
    X_train, X_test, y_train, y_test = run_feature_pipeline()

    # Load trained model
    model = joblib.load("src/models/best_model_tuned.pkl")

    # =========================
    # SHAP ANALYSIS
    # =========================
    explainer = shap.Explainer(model, X_train)

    shap_values = explainer(X_test)

    shap.summary_plot(shap_values, X_test, show=False)

    plt.savefig("src/evaluation/shap_summary.png")

    print("SHAP summary plot saved")

    # =========================
    # ERROR ANALYSIS
    # =========================
    y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt="d")
    plt.title("Error Analysis Heatmap")

    plt.savefig("src/evaluation/error_heatmap.png")

    print("Error heatmap saved")


if __name__ == "__main__":
    run_shap()