# Exploratory Data Analysis (EDA) Report

## 1. Dataset Overview

Dataset used: **Titanic Passenger Dataset**

The dataset contains passenger information such as passenger class, gender, age, fare, and survival status from the Titanic disaster.

* **Number of records:** 561
* **Number of features:** 12

### Features in the Dataset

* PassengerId
* Survived (Target Variable)
* Pclass
* Name
* Sex
* Age
* SibSp
* Parch
* Ticket
* Fare
* Cabin
* Embarked

The target variable **Survived** indicates whether a passenger survived the disaster.

---

# 2. Data Cleaning & Preprocessing

A data preprocessing pipeline was implemented in:

```
src/pipelines/data_pipeline.py
```

The following steps were performed:

### 1. Duplicate Removal

Duplicate records were checked and removed to ensure dataset integrity.

### 2. Missing Value Handling

Missing values were handled using the following strategy:

* **Numerical features:** filled using **median**
* **Categorical features:** filled using **mode**

After preprocessing, the dataset contains **no missing values**.

### 3. Outlier Detection and Removal

Outliers were detected using the **Interquartile Range (IQR) method** and removed to improve data quality.

The cleaned dataset was saved to:

```
src/data/processed/final.csv
```

---

# 3. Missing Values Analysis

A **missing values heatmap** was generated using the `missingno` library.

### Observation

* After preprocessing, **no missing values remain** in the dataset.
* All columns now contain complete data.

This confirms that the **data pipeline successfully handled missing data**.

---

# 4. Feature Distribution Analysis

Histograms were generated for all numerical features.

### Observations

* Some features show **skewed distributions**, particularly the **Fare** column.
* Passenger class and fare values show variations that may influence survival probability.
* Age distribution shows a wide range of passenger ages.

These distributions help identify patterns that may influence model performance during training.

---

# 5. Correlation Analysis

A **correlation matrix** was generated to analyze relationships between numerical features.

### Observations

* Some moderate correlations exist between numerical variables.
* Features such as **Pclass, Fare, and Age** may influence survival outcomes.

Correlation analysis helps identify features that may contribute to predictive models.

---

# 6. Target Variable Distribution

Target variable: **Survived**

Distribution:

* **Did Not Survive (0):** 400 passengers
* **Survived (1):** 161 passengers

### Observation

The dataset shows **class imbalance**, where the number of passengers who did not survive is significantly higher than those who survived.

This imbalance may need to be addressed during model training using techniques such as:

* class weighting
* resampling methods (e.g., SMOTE)

---

# 7. Conclusion

The dataset was successfully processed using a structured ML data pipeline.

Key outcomes:

* Raw dataset cleaned and processed
* Missing values handled
* Outliers removed
* EDA analysis performed
* Clean dataset generated for model training

The processed dataset is now ready for the next stage of the ML pipeline:

**Feature Engineering → Model Training → Evaluation → Deployment**
