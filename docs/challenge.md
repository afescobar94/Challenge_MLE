# Technical Notes & Fixes

## 1. Python Version Compatibility

The project was executed using **Python 3.11**, which required adjusting dependency versions to ensure compatibility:

```txt
numpy>=1.24,<2.0
pandas>=1.5.3,<2.0
```

This change avoids compatibility issues with newer versions of these libraries.

---

## 2. Seaborn Plot Fix

The following line in the notebook:

```python
sns.barplot(flights_by_airline.index, flights_by_airline.values, alpha=0.9)
```

Was updated to:

```python
sns.barplot(x=flights_by_airline.index, y=flights_by_airline.values, alpha=0.9)
```

Reason:
Seaborn requires the use of keyword arguments (`x=`, `y=`) instead of positional arguments.

---

## 3. Dependency Update

The following dependency was added to `requirements.txt`:

```txt
xgboost
```

This was necessary for training and evaluating gradient boosting models.

---

## 4. Delay Rate Calculation Fix

The original implementation incorrectly computed the delay rate as:

- `total / delays`

This is not a valid rate. It was corrected to properly reflect:

- `delays / total`

---

## 5. High Season Calculation Fix

The limits used to compute `is_high_season` were adjusted to correctly include the start and end of each day, ensuring accurate classification of flights within seasonal boundaries.

---

## 6. Unused Variable Fix

The variable `training_data` was defined but not used in one of the previous versions.
This was corrected to ensure consistency and avoid dead code.

---

## 7. Model Selection Rationale

This is a highly imbalanced classification problem, where:

- Most flights -> no delay
- Few flights -> delay

### Models Without Class Balancing (Discarded)

- Recall ~= 0.01 -> almost no delays detected
- Accuracy ~= 0.81 -> misleading

These models predict almost everything as "no delay", making them useless in practice.

### Models With Class Balancing (Selected Candidates)

#### XGBoost + Balance

- Precision: 0.25
- Recall: 0.69
- F1 Score: 0.37
- Accuracy: 0.55

#### Logistic Regression + Balance

- Precision: 0.25
- Recall: 0.69
- F1 Score: 0.36
- Accuracy: 0.55

Both models show very similar performance.

### Final Model Selection

Selected model:

- XGBoost + top10 features + class balancing

Reasons:

- Comparable performance to Logistic Regression
- Better ability to capture non linear relationships
- More robust and scalable for future improvements

Model behavior interpretation:

- Detects 69% of delays
- Produces false positives (precision = 0.25)

Trade-off:

- The model prioritizes recall over precision
- It is preferable to flag potential delays rather than miss real delays

---

## 8. Local Setup and Test Execution

To run the project locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

To run the required tests:

```bash
make model-test
make api-test
```

To run stress tests:

```bash
make stress-test
```

Note:
Before `make stress-test`, update `STRESS_URL` in `Makefile` to point to the deployed API URL.

---

## 9. API Local Run (Without Docker)

To run the API directly with Uvicorn:

```bash
uvicorn challenge.api:app --host 0.0.0.0 --port 8000 --reload
```

Health check:

```bash
curl http://localhost:8000/health
```

Prediction example:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"flights":[{"OPERA":"Aerolineas Argentinas","TIPOVUELO":"N","MES":3}]}'
```

---

## 10. Docker Build, Run and Stop

The project already includes Docker support via `Dockerfile` and `Makefile`.

### Build image

```bash
make docker-build
```

### Run container

```bash
make docker-run
```

### Stop and remove container

```bash
make docker-stop
```

## 12. CI/CD Status
