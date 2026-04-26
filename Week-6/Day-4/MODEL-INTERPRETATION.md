# Model Interpretation & Tuning

## Best Model Selection (Day 3)

Four models were trained:
- Logistic Regression
- Random Forest
- XGBoost
- Neural Network

Based on 5-fold cross-validation ROC-AUC score, **Logistic Regression** performed best and was selected for further tuning.

---

## Hyperparameter Tuning (Day 4)

Optuna was used to tune Logistic Regression.

### Tuned Parameters:
- C (regularization strength)
- Penalty (L1 / L2)

### Objective:
Maximize ROC-AUC using 5-fold cross-validation.

---

## Performance Comparison

| Metric | Before Tuning | After Tuning |
|-------|-------------|-------------|
| ROC-AUC | 0.74 | 0.81 |
| Accuracy | 0.80 | 0.84 |

👉 The tuned model shows improved generalization performance.

---

## Feature Importance

Logistic Regression coefficients were used to determine feature importance.

- Positive coefficients → Increase survival probability
- Negative coefficients → Decrease survival probability

---

## SHAP Explainability

SHAP values were used to interpret predictions.

### Outputs:
- SHAP Summary Plot
- SHAP Feature Importance

These explain:
- Global feature impact
- Individual prediction behavior


## Error Analysis

Confusion matrix was used to analyze model errors:
- False Positives
- False Negatives

Heatmap visualization was generated.

---

## Conclusion

- Logistic Regression was the best baseline model
- Hyperparameter tuning improved performance
- Model is interpretable and explainable using SHAP