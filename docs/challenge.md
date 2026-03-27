# Technical Notes & Fixes

## 1. Python Version Compatibility

The project was executed using **Python 3.11**, which required adjusting dependency versions to ensure compatibility:

numpy>=1.24,<2.0
pandas>=1.5.3,<2.0


This change avoids compatibility issues with newer versions of these libraries.

---

## 2. Seaborn Plot Fix

The following line in the notebook:

```python
sns.barplot(flights_by_airline.index, flights_by_airline.values, alpha=0.9)

Was updated to:

sns.barplot(x=flights_by_airline.index, y=flights_by_airline.values, alpha=0.9)
```
Reason:
Seaborn requires the use of keyword arguments (x=, y=) instead of positional arguments.

## 3. Dependency Update

The following dependency was added to requirements.txt
```
xgboost
```
This was necessary for training and evaluating gradient boosting models.

## 4. Delay Rate Calculation Fix

The original implementation incorrectly computed the delay rate as:

* total / delays

This is not a valid rate. It was corrected to properly reflect:

* delays / total

## 5. High Season Calculation Fix

The limits used to compute is_high_season were adjusted to correctly include the start and end of each day, ensuring accurate classification of flights within seasonal boundaries.

## 6. Unused Variable Fix

The variable training_data was defined but not used.
This was corrected to ensure consistency and avoid dead code.

## 7. Model Selection Rationale

This is a highly imbalanced classification problem, where:

Most flights → no delay

Few flights → delay

* Models Without Class Balancing (Discarded)

Recall ≈ 0.01 → almost no delays detected

Accuracy ≈ 0.81 → misleading

* These models predict almost everything as “no delay”, making them useless in practice.

###  Models With Class Balancing (Selected Candidates)

XGBoost + Balance

Precision: 0.25

Recall: 0.69

F1 Score: 0.37

Accuracy: 0.55

### Logistic Regression + Balance

Precision: 0.25

Recall: 0.69

F1 Score: 0.36

Accuracy: 0.55

* Both models show very similar performance

### Final Model Selection

Selected model:

XGBoost + top10 features + class balancing


* Comparable performance to Logistic Regression

* Better ability to capture non linear relationships

* More robust and scalable for future improvements

* Model Behavior Interpretation

* Detects 69% of delays

* Produces false positives (precision = 0.25)

### Trade-off:

* The model prioritizes recall over precision

* This means it is preferable to flag potential delays rather than miss real delays