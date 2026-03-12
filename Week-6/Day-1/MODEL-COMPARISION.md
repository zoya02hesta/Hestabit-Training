# Model Comparison

Four models were trained:

1. Logistic Regression
2. Random Forest
3. XGBoost
4. Neural Network

Evaluation metrics:
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

5-fold cross-validation was used.

The best model was automatically selected based on ROC-AUC score.

The final model was saved as:
src/models/best_model.pkl