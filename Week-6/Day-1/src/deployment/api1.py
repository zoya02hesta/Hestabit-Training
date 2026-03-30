from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import pickle
import os
import warnings

warnings.filterwarnings("ignore")

app = FastAPI()

# -------------------------
# Load Model + Features
# -------------------------
BASE_DIR = os.path.dirname(__file__)

model_path = os.path.join(BASE_DIR, "../models/model.pkl")
feature_path = os.path.join(BASE_DIR, "../models/feature_list.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(feature_path, "rb") as f:
    feature_list = pickle.load(f)

# -------------------------
# Input Schema (Validation)
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
# Home Route
# -------------------------
@app.get("/")
def home():
    return {"message": "Titanic Survival Prediction API 🚀"}

# -------------------------
# Predict Route
# -------------------------
@app.post("/predict")
def predict(data: PassengerInput):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([data.dict()])

        # -------------------------
        # SAME preprocessing as training
        # -------------------------

        # Encode Sex
        df["Sex"] = df["Sex"].map({"male": 1, "female": 0})

        # Fill missing values
        df["Age"].fillna(30, inplace=True)
        df["Embarked"].fillna("S", inplace=True)

        # One-hot encoding
        df = pd.get_dummies(df, columns=["Embarked"], drop_first=True)

        # -------------------------
        # Align with training features
        # -------------------------
        df = df.reindex(columns=feature_list, fill_value=0)

        # -------------------------
        # Prediction
        # -------------------------
        prediction = model.predict(df)[0]
        proba = model.predict_proba(df)[0][1]

        result = "Survived" if prediction == 1 else "Did Not Survive"

        return {
            "prediction": int(prediction),
            "result": result,
            "confidence": round(float(proba), 2)
        }
        

    except Exception as e:
        return {"error": str(e)}