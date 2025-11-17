# DevOps Assignment Report: ML-Ops CI/CD Pipeline

Student: Sarra Dhouaifi
Class : CI2
Repository Link: https://github.com/besmaguesmi/DevOps-MLOps-Labs

## Task 1: Prepare the ML Project

### 1. Fork the repository

I began by forking the provided source repository to my personal GitHub account. 
![alt text](Task1.1.1.png)
![alt text](Task1.1.2.png)
![alt text](Task1.1.3.png)

### 2. Inspect the repo structure
After forking, I cloned the repo locally using git clone and navigated into the folder session2/ml-app to inspect the file structure.
I verified that the project contains:   src/ folder and requirements.txt

Cloning the project : ![alt text](Task1.1.4.png)
Inspecting the repo structure and makeing sure requirements.txt exists : ![alt text](Task1.2.png)

## Task 2: Run the app locally

### 1. Create a virtual environment & install dependencies
From inside session2/ml-app, I created and activated a virtual environment:
Installing Dependencies: ![alt text](Task2.png)

I executed the training script: This successfully generated:    models/iris_classifier.pkl
                                                                plots (confusion matrix, feature importance)
![alt text](Task2.1.2.png)

## Task 3: Write Unit Tests

### 1 & 2. Create tests/ folder with meaningful tests
The repository already contained a tests/test_model.py file with 6 meaningful unit tests, which was more than the 3 required. 

These tests verify:
Model initialization (test_model_initialization)

Model training (test_model_training)

Model prediction (test_model_prediction)

Model evaluation (test_model_evaluation)

Saving and loading the model (test_model_save_load)

Data loading (test_data_loading)

### 3. Running tests with pytest
![alt text](Task3.png)

## Task 4: Linting & Formatting
### 1. Add a linter a minimal config.
I installed the linter and created a .flake8 file : 
![alt text](Task4.1.png)
![alt text](Task4.2.png)
### 2. Ensure flake8 runs and the code meets basic style checks.
![alt text](Task4.3.png)

## Task 5: GitHub Actions CI Workflow
I created .github/workflows/ci.yml to automate: Checkout
                                                Setup Python
                                                Install dependencies
                                                Run flake8
                                                Run pytest
                                                Upload test results
                                                Build Docker image
                                                Upload Docker artifact
The pipeline ran successfully on GitHub.
![alt text](Task5.1.png)
![alt text](Task5.1.2.png)
![alt text](Task5.2.png)

## Task 6: Containerize the Application
Build Docker Image : 
![alt text](Task6.1.png)

Run the Training Model inside Docker : 
![alt text](Task6.2.png)
![alt text](Task6.3.png)