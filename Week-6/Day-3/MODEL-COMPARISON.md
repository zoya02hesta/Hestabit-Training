# Model Comparison Report

## 📌 Overview

This project implements a machine learning pipeline for predicting Titanic survival using multiple models. The goal was to compare performance across models and automatically select the best one.

---

## ⚙️ Models Trained

The following models were trained:

1. Logistic Regression
2. Random Forest
3. Gradient Boosting
4. Neural Network (MLPClassifier)

---

## 🔁 Training Strategy

* Data split: **80% train / 20% test**
* Cross-validation: **5-Fold Cross Validation**
* Evaluation metric for selection: **ROC-AUC Score**
* Additional metrics:

  * Accuracy
  * Precision
  * Recall
  * F1 Score

---

## 📊 Evaluation Metrics

All model metrics are stored in:

```
src/evaluation/metrics.json
```

Each model includes:

* accuracy
* precision
* recall
* f1 score
* roc_auc
* cv_roc_auc_mean

---

## 🏆 Best Model Selection

The best model is selected based on:

> **Highest ROC-AUC score on the test dataset**

This ensures better performance for imbalanced classification problems.

The selected model is automatically saved as:

```
src/models/best_model.pkl
```

---

## 📈 Cross-Validation

To avoid overfitting and ensure robustness:

* 5-fold cross-validation is applied on training data
* Mean ROC-AUC across folds is computed
* Compared against test ROC-AUC

---

## 📉 Confusion Matrix

A confusion matrix is generated for the best model to evaluate:

* True Positives
* True Negatives
* False Positives
* False Negatives

This helps in understanding model performance beyond accuracy.

---

## 🧠 Feature Engineering

The following preprocessing steps were applied:

* Dropped irrelevant columns:

  * PassengerId, Name, Ticket, Cabin
* Missing value handling:

  * Age → median
  * Embarked → mode
* Encoding:

  * Sex → binary encoding
  * Embarked → one-hot encoding

---

## 💾 Artifacts Generated

| File               | Description                   |
| ------------------ | ----------------------------- |
| `best_model.pkl`   | Final selected model          |
| `feature_list.pkl` | Features used during training |
| `metrics.json`     | Performance of all models     |

---

## 🚀 Key Learnings

* Model comparison is essential before deployment
* ROC-AUC is a better metric than accuracy for classification
* Cross-validation prevents overfitting
* Feature engineering significantly impacts model performance

---

## ✅ Conclusion

A complete multi-model training pipeline was built with:

✔ Multiple models
✔ Cross-validation
✔ Performance comparison
✔ Automatic best model selection
✔ Artifact saving for deployment

This pipeline is production-ready and can be extended with hyperparameter tuning and monitoring.
