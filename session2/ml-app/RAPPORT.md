# REPORT – DevOps ML Project

### Task 1 — Prepare the ML Project
1. **Fork the Repository**

I successfully forked the original repository besmaguesmi/DevOps-MLOps-Labs into my personal GitHub account under the name Chamakh1/DevOps-MLOps-Labs.  
This completes the forking step.

**Screenshots:**  
![alt text](./images/fork.PNG)  
![alt text](./images/fork2.PNG)

---

2. **Inspect the Repository**

After cloning the forked repository locally, I explored its directory structure to verify that all required components were present.

I confirmed that the project includes a requirements.txt file, which contains the necessary Python dependencies such as:

- scikit-learn  
- pandas  
- flake8  
- pytest  
- joblib  

This ensures that the project environment can be correctly set up for development, testing, and CI/CD workflow automation.

---

### Task 2: Run the app locally

1. **Cloned the forked repository to my local machine**

![alt text](./images/git%20clone%20repo.PNG)

---

2. **Created a Python virtual environment**

Command attempted:

```
source .venv/bin/activate
```

This command is for Linux and caused an error on Windows:

![alt text](./images/error%201%20venv.PNG)

Correct Windows command:

```
.env\Scriptsctivate
```

![alt text](./images/correction%20error%201%20venv.PNG)

---

3. **Installed all dependencies**  
Command: `pip install -r requirements.txt`

---

### **Addendum: Resolving Local Environment Build Error**

While executing Task 2 (`pip install -r requirements.txt`), I encountered a significant build error:

```
DistutilsPlatformError: Microsoft Visual C++ 14.0 or greater is required.
```

**Analysis:**  
This error occurred because pip could not find a pre-compiled binary (.whl) for `scikit-learn==1.3.0` compatible with Python 3.12.  
It therefore attempted to build from source, which requires Microsoft C++ Build Tools.

![alt text](./images/error%202%20install%20requirement%201.PNG)  
![alt text](./images/error%20requirement%202.PNG)

---

### **Resolution**

To fix this and follow DevOps best practices (align local and CI environments):

1. Installed **Python 3.10**  
2. Deleted the previous, broken `.venv`  
3. Created a new virtual environment using Python 3.10:  
   ```
   python -m venv .venv
   ```
4. Activated it:
   ```
   .\.venv\Scriptsctivate
   ```
5. Reinstalled dependencies:
   ```
   pip install -r requirements.txt
   ```

Installation completed successfully:

![alt text](./images/sol%20requirments.PNG)

---

4. **Ran the model training script**

Command:
```
python src/train.py
```

The script successfully:

- Loaded the Iris dataset  
- Trained a Logistic Regression model  
- Achieved **96.7% accuracy**  
- Saved:
  - `iris_classifier.pkl`
  - `confusion_matrix.png`
  - `feature_importance.png`

![alt text](./images/run%20train.PNG)

---

### Task 3: Unit Testing

I discovered a pre-existing `tests/` directory.  
To ensure a clean implementation, I deleted it and created a new `tests/test_model.py` from scratch.

I wrote **three pytest unit tests**:

1. **test_model_file_exists**  
   - Confirms that `train.py` successfully generates `models/iris_classifier.pkl`.

2. **test_model_loading_and_type**  
   - Loads the saved model with joblib  
   - Checks attributes `.predict()` and `.coef_`

3. **test_data_loading**  
   - Verifies dataset shapes:  
     - data: (150, 4)  
     - target: (150,)

---

### **Test Execution Results**

```
========================= test session starts =========================
platform win32 -- Python 3.10.11, pytest-7.3.1, pluggy-1.6.0
rootdir: C:\...
collected 3 items
tests	est_model.py ... [100%]
========================== 3 passed in 1.31s ==========================
```

![alt text](./images/test.PNG)

---

### Task 4: Linting & Formatting

I integrated **flake8** to enforce code quality.

1. Created `.flake8` config  
2. Ran:
   ```
   flake8 .
   ```
3. Many violations were found:

---

### **Analysis of Linting Errors**

- **F401** unused imports  
- **E302/E305** spacing issues  
- **F541** f-string without placeholders  
- **W291/W292** whitespace issues  

![alt text](./images/flake8.PNG)

---

### **Resolution**

I manually corrected all issues:

- Removed unused imports  
- Added spacing between functions  
- Fixed f-string misuse  
- Removed trailing whitespace  

A second run showed **0 errors**:

![alt text](./images/sol%20flake.PNG)

---

### Task 5: GitHub Actions CI Workflow

I implemented the CI pipeline using GitHub Actions.

---

### **Initial Setup and Challenges**

I found an existing `ci.yml` at the root, deleted it, and created a new workflow.

After pushing, the workflow failed:

![alt text](./images/task%205%20push.PNG)

---

### **Analysis of the First Failure**

The failure occurred because:

1. My initial workflow was **multi-job** (test, train-model, deploy-docs)  
2. Tests ran **before** the model was trained  
3. The workflow file was placed at:
   ```
   session2/ml-app/.github/workflows/ci.yml
   ```
   so GitHub Actions did not detect it.

![alt text](./images/task%205%20workflow%20failed.png)

---

### **Solution and Successful Implementation**

Key fixes:

1. Moved workflow to:
   ```
   .github/workflows/ci.yml
   ```
2. Created a **single job** workflow:  
   `build-lint-test-and-dockerize`
3. Added:  
   ```
   defaults.run.working-directory: ./session2/ml-app
   ```
4. Step order:
   1. Checkout  
   2. Setup Python  
   3. Install dependencies  
   4. Lint with flake8  
   5. Run training script  
   6. Run tests  
   7. Build Docker image  

After pushing, the workflow passed:

![alt text](./images/task5%20workflow%20passe.PNG)

---

### Task 6: Containerise the App

I created a Dockerfile based on **python:3.10-slim**.

---

### **1. Build the Image**

Command:

```
docker build -t devops-ml-app .
```

![alt text](./images/task%206%20build.PNG)  
![alt text](./images/task%206%20build1.PNG)

---

### **2. Run the Container**

Command:

```
docker run devops-ml-app
```

The container executed the training script successfully.  
Output:

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

---
