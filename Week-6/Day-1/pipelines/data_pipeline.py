import pandas as pd
import numpy as np
from pathlib import Path

RAW_PATH = "src/data/raw/dataset.csv"
PROCESSED_PATH = "src/data/processed/final.csv"

def load_data():
    df = pd.read_csv(RAW_PATH)
    print("Data loaded successfully")
    return df

def remove_duplicates(df):
    df = df.drop_duplicates()
    print("Duplicates removed")
    return df

def handle_missing(df):
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])

    print("Missing values handled")
    return df

def remove_outliers(df):
    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df = df[(df[col] >= lower) & (df[col] <= upper)]

    print("Outliers removed")
    return df

def save_data(df):
    Path("src/data/processed").mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print("Processed dataset saved")

def run_pipeline():
    df = load_data()
    df = remove_duplicates(df)
    df = handle_missing(df)
    df = remove_outliers(df)
    save_data(df)

if __name__ == "__main__":
    run_pipeline()
