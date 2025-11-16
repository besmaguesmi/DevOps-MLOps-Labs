
# Task 1 — Prepare the ML Project

## 1. Fork the Repository

I successfully forked the original repository **besmaguesmi/DevOps-MLOps-Labs** into my personal GitHub account under the name **Chamakh1/DevOps-MLOps-Labs**.  
This completes the forking step.

![alt text](./images/fork.PNG)  
![alt text](./images/fork%202.PNG)

## 2. Inspect the Repository

After cloning the forked repository locally, I explored its directory structure to verify that all required components were present.

I confirmed that the project includes a **requirements.txt** file, which contains the necessary Python dependencies such as:

- scikit-learn  
- pandas  
- flake8  
- pytest  
- joblib  

This ensures that the project environment can be correctly set up for development, testing, and CI/CD workflow automation.

# Task 2 — Run the App Locally

## 1. Cloned the forked repository to my local machine. 

![alt text](./images/git%20clone%20repo.PNG)

## 2. Create the virtual environment

I attempted to activate a virtual environment using the Linux command:

```
source .venv/bin/activate
```

This resulted in an error on Windows:

![alt text](./images/error%201%20venv.PNG)

The correct Windows command is:

```
.env\Scriptsctivate
```

![alt text](./images/correction%20error%201%20venv.PNG)

## 3. Install all dependencies

`pip install -r requirements.txt`

## Addendum: Resolving Local Environment Build Error

During installation, I encountered the following error:

**DistutilsPlatformError: Microsoft Visual C++ 14.0 or greater is required**

This occurred because scikit-learn==1.3.0 does not provide a wheel for Python 3.12, so pip attempted to build from source.

![alt text](./images/error%202%20install%20requirement%201.PNG)  
![alt text](./images/error%20requirement%202.PNG)

### Resolution

To fix this issue and follow DevOps best practices, I aligned my local environment with the CI environment (Python 3.10):

1. Installed Python 3.10  
2. Deleted the non-functional `.venv`  
3. Created a fresh virtual environment using Python 3.10  
4. Activated the environment  
5. Reinstalled the dependencies  

![alt text](./images/sol%20requirments.PNG)

## 4. Run the training script

`python src/train.py`

The model trained successfully with **96.7% accuracy**, saved its artifacts, and generated plots.

![alt text](./images/run%20train.PNG)

# Task 3 — Unit Testing

I discovered a pre-existing `tests/` directory in the project. To ensure a clean implementation, I deleted this old folder and created a new `tests/test_model.py` file.

I wrote **three unit tests** using pytest:

1. `test_model_file_exists` – verifies the artifact `iris_classifier.pkl` is generated  
2. `test_model_loading_and_type` – checks model integrity using joblib  
3. `test_data_loading` – validates data shape from `load_iris()`  

### Test Execution Results

All tests passed successfully.

```
========================= test session starts =========================
platform win32 -- Python 3.10.11, pytest-7.3.1, pluggy-1.6.0
rootdir: C:\...
collected 3 items
tests	est_model.py ... [100%]
========================== 3 passed in 1.31s ==========================
```

![alt text](./images/test.PNG)

# Task 4 — Linting and Formatting

I integrated flake8 for code quality.

1. Created a `.flake8` configuration  
2. Ran `flake8 .`  
3. Fixed all reported issues  

### Linting Issues Found

- F401 unused imports  
- E302 / E305 wrong spacing  
- F541 f-string without placeholders  
- W291/W292 whitespace errors  

![alt text](./images/flake8.PNG)

### After Fixing

`flake8 .` returned no errors.

![alt text](./images/sol%20flake.PNG)

# Task 5 — GitHub Actions CI Workflow

I implemented the CI workflow using GitHub Actions.

### Initial Issues

- There was an old `ci.yml` at the wrong location  
- My first workflow had multiple jobs and incorrect job order  
- Tests failed because the model had not been generated yet  

![alt text](./images/task%205%20push.PNG)  
![alt text](./images/task%205%20workflow%20failed.png)

## Final Solution

I applied several fixes:

1. Corrected workflow file location  
2. Rebuilt the workflow as a **single job**  
3. Set working directory to `session2/ml-app`  
4. Ordered steps correctly (lint → train → test → docker build)  

After pushing updates, the workflow executed successfully.

![alt text](./images/task5%20workflow%20passe.PNG)

# Task 6 — Containerise the App

I created a Dockerfile based on `python:3.10-slim`.

## 1. Build the image

`docker build -t devops-ml-app .`

![alt text](./images/task%206%20build.PNG)  
![alt text](./images/task%206%20build1.PNG)

## 2. Run the container

`docker run devops-ml-app`

### Container Run Log:

```
Starting Iris Classifier Training...
Loading Iris dataset...
Successfully loaded Iris dataset
   Features: 4, Samples: 150
   Training set: 120 samples
   Test set: 30 samples
   Classes: [0 1 2]
...
Model Accuracy: 0.9667

Classification Report:
              precision    recall  f1-score   support

           0       1.00      1.00      1.00        10
           1       1.00      0.90      0.95        10
           2       0.91      1.00      0.95        10

    accuracy                           0.97        30
   macro avg       0.97      0.97      0.97        30
weighted avg       0.97      0.97      0.97        30

...
Training completed successfully!
Model saved to: models/iris_classifier.pkl
Plots saved: confusion_matrix.png, feature_importance.png
```

![alt text](./images/task%206%20run%20image.PNG)
