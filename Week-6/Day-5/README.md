# Titanic Survival Prediction API 🚀

## 📌 Overview

This project predicts whether a passenger survived the Titanic disaster using a Machine Learning model deployed with FastAPI.

## 🛠 Tech Stack

* Python
* Pandas
* Scikit-learn
* FastAPI

## 🚀 Run the Project

```bash
uvicorn src.deployment.api:app --reload
```

## 📡 API Endpoints

### GET /

Home route

### GET /health

Health check

### POST /predict

Predict survival

## 📥 Sample Input

```json
{
  "Pclass": 1,
  "Sex": "female",
  "Age": 25,
  "SibSp": 0,
  "Parch": 0,
  "Fare": 100,
  "Embarked": "C"
}
```

## 📤 Output

```json
{
  "prediction": 1,
  "result": "Survived",
  "confidence": 0.91
}
```
