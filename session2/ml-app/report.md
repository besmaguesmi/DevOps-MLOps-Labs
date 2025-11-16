# REPORT
## Running the App

Clone the repository and navigate to the project folder:

```
git clone https://github.com/saifallah1234/DevOps-MLOps-Labs.git
cd ml-app
```


Create a virtual environment and activate it:
```
python -m venv venv
.\venv\Scripts\activate    
```


Install the dependencies:
```
pip install -r requirements.txt
```

Run the training script:
```
python src/train.py
```
<img width="919" height="354" alt="image" src="https://github.com/user-attachments/assets/0ea29115-f00e-467f-bc17-779401f304e8" />

This will train the model and save it to the models/ folder.

Testing the Model

To test the model functionality:
```
pytest tests/test_model.py
```
<img width="1287" height="187" alt="image" src="https://github.com/user-attachments/assets/e4e3706e-a94a-4b39-be56-0404d5b24648" />

The tests check:

- Model initialization
- Model training
- Predictions
- Evaluation metrics
- Saving and loading of the model
- Data loading correctness
## Other tests implemented
By running 
```
pytest tests/test.py
```
<img width="1277" height="158" alt="image" src="https://github.com/user-attachments/assets/893ed705-31ae-4c79-a996-45ec9fd041a8" />

1. test_prediction_shape

Ensures that the model returns a prediction for every test sample.
Calls clf.predict(X_test)
Checks that:
```
preds.shape[0] == X_test.shape[0]
```
This prevents issues where the model outputs missing or partial predictions.

2. test_prediction_classes
   
Verifies that the predicted class labels are valid Iris classes: {0, 1, 2}.
Converts predictions to a set
Ensures it’s a subset of valid class IDs:
```
assert set(preds).issubset({0, 1, 2})
```
**Why it matters:**
Guarantees the classifier never outputs invalid or unexpected labels due to bugs, corrupted training, or incorrect preprocessing.

3. test_evaluate_returns_float_and_str

Checks the correct behavior of the evaluation method:
accuracy must be a float within [0, 1]
report must be a formatted string containing metrics (precision/recall/F1)
```
accuracy, report = clf.evaluate(...)
assert isinstance(accuracy, float)
assert 0 <= accuracy <= 1
assert isinstance(report, str)
assert "precision" in report.lower()
```
 **Why it matters:**
This ensures the evaluation output is consistent and compatible with downstream CI checks, API responses, or dashboards.

---
## Linting
A Flake8 configuration was added to enforce linting rules, setting a max line length of 250 and ignoring E203/W503 to ensure compatibility with Black formatting.  
The linter excludes virtual environments, cache folders, and test files to avoid unnecessary warnings and focus on application source code.

```
[flake8]
max-line-length = 250
ignore = E203, W503
exclude =
    venv/,
    __pycache__/,
    tests/

```
<img width="916" height="230" alt="image" src="https://github.com/user-attachments/assets/19ad8461-a5ff-424e-9b81-dca8093f1073" />
---
## CI/CD Implementation

### CI/CD Workflow Overview

We implemented a GitHub Actions workflow to automate testing, linting, and model training:
```
- **Triggering:** Runs on `push` to `main` or `develop`, and on `pull_request` to `main`.
- **Jobs:**
  1. **Test Job:**  
     - Checks out the code
     - Sets up Python (3.9 and 3.10)
     - Installs dependencies
     - Runs `pytest` to validate unit tests
     - Runs `flake8` to check code style
  2. **Train-Model Job:** (runs only on `main` branch)  
     - Depends on Test job
     - Trains the model
     - Uploads trained model and evaluation plots as artifacts
  3. **Deploy-Docs Job:** (runs only on `main`)  
     - Deploys documentation (placeholder in this project)
```
### Choices Made
```
- **Python Versions:** Tested on 3.9 and 3.10 to ensure compatibility.
- **Linting:** Used `flake8` for PEP8 compliance.
- **Artifacts:** Uploaded trained models and evaluation plots for reproducibility.
- **Dockerization:** Dockerfile added for containerized training.
```
---

## Running Locally with Docker

Build the Docker image:


```
cd session2/ml-app
docker build -t ml-app .
```
<img width="1277" height="370" alt="image" src="https://github.com/user-attachments/assets/e767adc6-5236-4554-a0f8-6d3714a0dd5d" />

Run the container:


```
docker run --rm -v {Path}/models:/app/models ml-app
```
<img width="1288" height="364" alt="image" src="https://github.com/user-attachments/assets/b7d33f2d-96b9-4167-b78b-627cd9de59a7" />

This will train the model inside a container and save artifacts to your local `models/` folder.

---

## CI/CD Behavior

When you push changes or create a pull request:
```
1. GitHub Actions triggers the CI workflow.
2. The test job runs first:
   - Runs unit tests
   - Checks code style
3. If tests pass and the branch is `main`, the training job runs:
   - Trains the model
   - Uploads models and evaluation plots as artifacts
4. Documentation deployment runs last (placeholder in this project).
```
<img width="1901" height="420" alt="image" src="https://github.com/user-attachments/assets/1a3adb6e-ca13-4163-9439-908dd1ddd3dc" />

