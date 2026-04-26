import json
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import SelectKBest
from build_features import run_feature_pipeline


def select_features():

    # Run feature pipeline
    X_train, X_test, y_train, y_test = run_feature_pipeline()

    # Select top 10 features
    selector = SelectKBest(score_func=mutual_info_classif, k=10)

    selector.fit(X_train, y_train)

    scores = selector.scores_

    # Plot feature importance
    plt.figure(figsize=(10,5))
    plt.bar(range(len(scores)), scores)
    plt.title("Feature Importance (Mutual Information)")
    plt.xlabel("Feature Index")
    plt.ylabel("Importance Score")

    plt.savefig("src/features/feature_importance.png")

    print("Feature importance graph saved")

    # Get selected features
    selected_features = selector.get_support()

    feature_list = [i for i, val in enumerate(selected_features) if val]

    # Save selected feature list
    with open("src/features/feature_list.json", "w") as f:
        json.dump(feature_list, f)

    print("Selected features saved")


if __name__ == "__main__":
    select_features()
