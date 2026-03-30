from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import numpy as np
import warnings
import uuid
import csv
from datetime import datetime

warnings.filterwarnings("ignore")

app = FastAPI()

# -------------------------
# Load Model + Features + Scaler
# -------------------------
BASE_DIR = os.path.dirname(__file__)

model_path = os.path.join(BASE_DIR, "../models/best_model_tuned.pkl")
feature_path = os.path.join(BASE_DIR, "../features/feature_list.pkl")
scaler_path = os.path.join(BASE_DIR, "../models/scaler.pkl")

model = joblib.load(model_path)
feature_columns = joblib.load(feature_path)

# Load scaler if exists
scaler = None
if os.path.exists(scaler_path):
    scaler = joblib.load(scaler_path)


# -------------------------
# Input Schema
# -------------------------
class PassengerInput(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str


# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health():
    return {"status": "OK"}


# -------------------------
# Home
# -------------------------
@app.get("/")
def home():
    return {"message": "Titanic Survival Prediction API 🚀"}


# -------------------------
# Feature Engineering Function (REUSABLE)
# -------------------------
def process_input(df):
    df = df.copy()

    df["Sex"] = df["Sex"].map({"male": 1, "female": 0})

    df["family_size"] = df["SibSp"] + df["Parch"]
    df["is_alone"] = (df["family_size"] == 0).astype(int)
    df["fare_per_person"] = df["Fare"] / (df["family_size"] + 1)
    df["age_fare_ratio"] = df["Age"] / (df["Fare"] + 1)
    df["age_squared"] = df["Age"] ** 2
    df["fare_log"] = np.log1p(df["Fare"])
    df["age_bucket"] = 0
    df["fare_bucket"] = 0
    df["pclass_fare"] = df["Pclass"] * df["Fare"]
    df["family_fare"] = df["family_size"] * df["Fare"]

    df = pd.get_dummies(df)

    df = df.reindex(columns=feature_columns, fill_value=0)

    # Apply scaling if available
    if scaler:
        df = scaler.transform(df)

    return df


# -------------------------
# Predict Route
# -------------------------
@app.post("/predict")
def predict(data: PassengerInput):

    try:
        input_df = pd.DataFrame([data.dict()])

        processed_df = process_input(input_df)

        prediction = model.predict(processed_df)[0]
        proba = model.predict_proba(processed_df)[0][1]

        result = "Survived" if prediction == 1 else "Did Not Survive"

        # -------------------------
        # LOGGING
        # -------------------------
        log_file = "prediction_logs.csv"

        request_id = str(uuid.uuid4())
        timestamp = datetime.now()

        log_row = [
            request_id,
            timestamp,
            data.Pclass,
            data.Sex,
            data.Age,
            data.SibSp,
            data.Parch,
            data.Fare,
            data.Embarked,
            int(prediction),
            float(proba)
        ]

        file_exists = os.path.exists(log_file)

        with open(log_file, "a", newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "request_id", "timestamp", "Pclass", "Sex", "Age",
                    "SibSp", "Parch", "Fare", "Embarked",
                    "prediction", "confidence"
                ])

            writer.writerow(log_row)

        return {
            "request_id": request_id,
            "prediction": int(prediction),
            "result": result,
            "confidence": round(float(proba), 2)
        }

    except Exception as e:
        return {"error": str(e)}