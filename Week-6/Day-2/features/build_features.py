import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = "src/data/processed/final.csv"


def load_data():
    return pd.read_csv(DATA_PATH)


# -------------------------
# Feature Engineering
# -------------------------
def build_features(df):

    df["family_size"] = df["SibSp"] + df["Parch"]
    df["is_alone"] = (df["family_size"] == 0).astype(int)

    df["fare_per_person"] = df["Fare"] / (df["family_size"] + 1)
    df["age_fare_ratio"] = df["Age"] / (df["Fare"] + 1)

    df["age_squared"] = df["Age"] ** 2
    df["fare_log"] = np.log1p(df["Fare"])

    df["age_bucket"] = pd.cut(df["Age"], bins=5, labels=False)
    df["fare_bucket"] = pd.cut(df["Fare"], bins=5, labels=False)

    df["pclass_fare"] = df["Pclass"] * df["Fare"]
    df["family_fare"] = df["family_size"] * df["Fare"]

    return df


# -------------------------
# Encoding
# -------------------------
def encode_categorical(df):

    categorical_cols = df.select_dtypes(include="object").columns

    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    return df


# -------------------------
# Split
# -------------------------
def split_data(df):

    y = df["Survived"]
    X = df.drop("Survived", axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test


# -------------------------
# Scaling (FIXED)
# -------------------------
def scale_features(X_train, X_test):

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 🔥 Convert back to DataFrame (VERY IMPORTANT)
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)

    # Save scaler for API
    os.makedirs("src/models", exist_ok=True)
    joblib.dump(scaler, "src/models/scaler.pkl")

    return X_train_scaled, X_test_scaled


# -------------------------
# Pipeline
# -------------------------
def run_feature_pipeline():

    df = load_data()

    # Basic cleaning (important for consistency)
    df.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1, inplace=True)

    df["Age"].fillna(df["Age"].median(), inplace=True)
    df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

    df["Sex"] = df["Sex"].map({"male": 1, "female": 0})

    df = build_features(df)

    df = encode_categorical(df)

    X_train, X_test, y_train, y_test = split_data(df)

    # Save FINAL feature list (correct place)
    os.makedirs("src/features", exist_ok=True)
    joblib.dump(X_train.columns.tolist(), "src/features/feature_list.pkl")

    X_train, X_test = scale_features(X_train, X_test)

    print("✅ Feature pipeline completed")

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    run_feature_pipeline()
