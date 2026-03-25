import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = "src/data/processed/final.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def build_features(df):

    # Example engineered features
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


def encode_categorical(df):

    categorical_cols = df.select_dtypes(include="object").columns

    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    return df


def scale_features(X_train, X_test):

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled


def split_data(df):

    y = df["Survived"]
    X = df.drop("Survived", axis=1)

    import joblib

    joblib.dump(X.columns.tolist(), "src/features/feature_list.pkl")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test


def run_feature_pipeline():

    df = load_data()

    df = build_features(df)

    df = encode_categorical(df)

    X_train, X_test, y_train, y_test = split_data(df)

    X_train, X_test = scale_features(X_train, X_test)

    print("Feature pipeline completed")

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    run_feature_pipeline()