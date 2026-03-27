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

The project now includes complete GitHub Actions workflows in:

- `.github/workflows/ci.yml`
- `.github/workflows/cd.yml`

### CI (`ci.yml`)

Trigger:

- `pull_request` to `main`
- `push` to `main`

Pipeline:

1. Install dependencies (`requirements-dev.txt`, `requirements-test.txt`, `requirements.txt`)
2. Run model tests (`make model-test`)
3. Run API tests (`make api-test`)
4. Build Docker image (`docker build ...`) as a build validation
5. Upload test artifacts from `reports/`

### CD (`cd.yml`)

Trigger:

- `push` to `main`
- manual execution (`workflow_dispatch`)

Pipeline:

1. Re-run tests before deployment
2. Validate Docker build on GitHub runner
3. Connect via SSH to AWS EC2
4. Update source code in server (`git pull --ff-only`)
5. Build Docker image in EC2
6. Recreate container (`airline-delay`) on port `8000`
7. Run health check and publish deployment details in workflow summary

### Required GitHub configuration

`Secrets`:

- `EC2_HOST`: Public IP or DNS of the EC2 instance
- `EC2_USER`: SSH user on the EC2 instance (for example, `ubuntu`)
- `EC2_SSH_KEY`: Private SSH key (PEM content) used by GitHub Actions to connect

`Variables` (optional, defaults included in workflow):

- `EC2_SSH_PORT` (default: `22`)
- `EC2_APP_PATH` (default: `/home/ubuntu/Challenge_MLE`)
- `IMAGE_NAME` (default: `challenge-mle:latest`)
- `CONTAINER_NAME` (default: `airline-delay`)
