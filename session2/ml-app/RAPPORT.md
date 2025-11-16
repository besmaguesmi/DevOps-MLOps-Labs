# DevOps Assignment Report: ML-Ops CI/CD Pipeline

Student: Tharaa Oueslati 
Class : CI1
Repository Link: https://github.com/besmaguesmi/DevOps-MLOps-Labs

## Task 1: Prepare the ML Project

1. Fork the repository
I began by forking the provided source repository to my personal GitHub account. My forked repository is available at httpsa://github.com/besmaguesmi/DevOps-MLOps-Labs.

Forked Repository on GitHub : ![alt text](<Capture d'écran 2025-11-15 191117.png>)

2. Inspect the repo structure
After forking, I cloned the repository to my local machine using git clone. I then navigated into the project directory (session2/ml-app) and inspected the file structure. I confirmed the presence of the src folder, which contains all the Python application logic, and the requirements.txt file, which lists the project's dependencies.

Cloning the project :  ![alt text](<Capture d'écran 2025-11-15 191620.png>)

Inspecting the repo structure and makeing sure requirements.txt exists : ![alt text](<Capture d'écran 2025-11-15 191716.png>)

## Task 2: Run the app locally

1. Create a virtualenv and install requirements
From within the session2-ml-app directory, I created a Python virtual environment using python -m venv .venv and activated it using .venv\Scripts\activate.

I then attempted to install the dependencies with pip install -r requirements.txt : ![alt text](<Capture d'écran 2025-11-15 192333.png>)

Decision / Error Faced: scikit-learn build failure
The installation immediately failed. The log showed that pip was trying to build scikit-learn==1.3.0 from source, which required "Microsoft Visual C++ 14.0 or greater". This led to a ModuleNotFoundError: No module named 'sklearn' when trying to run the app.

![alt text](<Capture d'écran 2025-11-15 192333-1.png>)

To fix this without installing the large C++ Build Tools, I edited the requirements.txt file. I removed the strict version pinning (e.g., ==1.3.0) for scikit-learn, pandas, and numpy. ![alt text](<Capture d'écran 2025-11-15 200654.png>)

This allowed pip to download newer, pre-compiled "wheel" files (.whl), which installed successfully.
![alt text](<Capture d'écran 2025-11-15 200715.png>)


2. Confirm the app runs
The assignment required running train.py and a web app.

Train Model: I ran python src/train.py, which executed successfully, creating a models/iris_classifier.pkl file.

Run App: The original src/predict.py was not a web app; it just printed examples. The assignment requires a web app (it mentions "endpoints" and "app port"). Therefore, I modified src/predict.py to be a complete Flask web server.

After modification, I ran python src/predict.py, which successfully started the web server on http://127.0.0.1:5000.

Training Script Output : ![alt text](<Capture d'écran 2025-11-16 133626.png>)

Web Server Running : ![alt text](<Capture d'écran 2025-11-16 133643.png>)

2. How to test endpoints
To test the endpoint, I opened a new PowerShell terminal.

Decision / Error Faced: curl command failure
I first tried the Linux-style curl -X POST ... command. This failed with the error Impossible de trouver un paramètre correspondant au nom «X» (Cannot find a parameter matching the name 'X').

I realized this is because curl in PowerShell is an alias for Invoke-WebRequest, which has different syntax. The correct PowerShell command for testing JSON APIs is Invoke-RestMethod.

Fix: I used the following Invoke-RestMethod command, which successfully connected to my running server and returned a JSON prediction.

Invoke-RestMethod -Uri [http://127.0.0.1:5000/predict](http://127.0.0.1:5000/predict) -Method Post -ContentType "application/json" -Body '{"features": [5.1, 3.5, 1.4, 0.2]}'


Successful Endpoint Test : ![alt text](<Capture d'écran 2025-11-15 204432.png>)

## Task 3: Write unit tests

1 & 2. Add a tests/ folder with meaningful tests
The repository already contained a tests/test_model.py file with 6 meaningful unit tests, which was more than the 3 required. These tests verify:

Model initialization (test_model_initialization)

Model training (test_model_training)

Model prediction (test_model_prediction)

Model evaluation (test_model_evaluation)

Saving and loading the model (test_model_save_load)

Data loading (test_data_loading)

3. Ensure tests run locally with pytest
When I first ran pytest, it failed with a ModuleNotFoundError: No module named 'src'.

Decision / Error Faced: pytest import error
The pytest command could not find the src folder as a package.

Fix: I applied a two-part fix:

I created an empty file named src/__init__.py. This tells Python to treat the src folder as a package.

I created a pytest.ini file in the root directory and added pythonpath = . to it. This tells pytest to look for packages in the current directory, allowing it to find src.

After these changes, I ran pytest again, and all 6 tests passed.

pytest Successful Run : ![alt text](<Capture d'écran 2025-11-16 134143.png>)

## Task 4: Linting & formatting

1. Add a linter and minimal config
I installed flake8 using pip install flake8. I then created a .flake8 configuration file in the project root to ignore a few non-critical errors (like E501 - line too long, E402 - module import error) and to exclude the .venv folder.

2. Ensure flake8 runs and code meets checks
I ran flake8 src tests, which produced a long list of style errors (F401 - unused imports, E302 - missing blank lines, etc.).

Decision: As required by the task, I went through all the files (data_loader.py, model.py, predict.py, train.py, utils.py, test_model.py) and manually fixed every linting error. This involved removing unused imports, adding the correct number of blank lines, and fixing whitespace.

After fixing all the errors, I ran flake8 src tests again. This time, it ran silently, producing no output, which confirms the code now meets the style checks.

flake8 Running before fixing : ![alt text](<Capture d'écran 2025-11-15 212201.png>)
flake8 Running before fixing : ![alt text](<Capture d'écran 2025-11-15 213714.png>)

## Task 5: GitHub Actions CI workflow

1. Create .github/workflows/ci.yml
I created the file at .github/workflows/ci.yml and configured it to run on both push and pull_request to the main branch.

2. Workflow Steps
My ci.yml workflow performs all the required steps in order:

Checkout code: Uses actions/checkout@v4.

Set up Python: Uses actions/setup-python@v5 to install Python 3.10.

Install dependencies: Installs pip, setuptools, and all packages from requirements.txt, as well as flake8, pytest, and flask.

Run the linter: Runs flake8 src tests --count --statistics, which will fail the build if any style errors are found.

Run tests and produce artifacts: Runs pytest --junitxml=test-results/junit.xml to execute tests and generate a JUnit XML report.

Upload test artifact: Uses actions/upload-artifact@v4 to save the junit.xml report.

Build a Docker image: Runs docker build . --file Dockerfile ... to build the image (requires the Dockerfile from Task 6).

Upload the image artifact: Saves the built image as app-image.tar and uploads it as a build artifact.

![alt text](<Capture d'écran 2025-11-15 213829.png>)

This workflow fully automates the project's quality checks. After pushing all my code, the pipeline ran and succeeded.

Successful GitHub Actions Pipeline : ![alt text](<Capture d'écran 2025-11-16 144040.png>)

## Task 6: Containerise the app

1. Add a Dockerfile
The repository had an existing Dockerfile, but it was incorrect. It only ran src/train.py and did not expose any ports.

Decision: I replaced it with a new, multi-stage Dockerfile. This new file:
- Starts from a lean python:3.10-slim image.
- Installs all dependencies (including flask).
- Copies only the src code into the container (a best practice).
- EXPOSE 5000 to open the application's port.
- Sets the CMD ["python", "src/predict.py"] to run the web server, fulfilling the "runnable container" requirement.

2. Build the docker image
I started Docker Desktop. I then ran docker build -t ml-app ., which successfully built the image.

Successful docker build :  ![alt text](<Capture d'écran 2025-11-16 135716.png>)

3. Run the training and the app using Docker
This was a multi-step process.

Run Training: I used a volume to save the trained model from the container to my local disk.
I used this command :
docker run --rm -v "$(pwd)\models:/app/models" ml-app python src/train.py

Running Training in Docker : ![alt text](<Capture d'écran 2025-11-16 115023.png>)

Run Web App: Next, I ran the web server, mapping the port and mounting the same volume to read the model:
docker run --rm -p 5000:5000 -v "$(pwd)\models:/app/models" ml-app

Running Web App in Docker : ![alt text](<Capture d'écran 2025-11-16 115134.png>)

Test Container: Finally, I opened a second terminal and used Invoke-RestMethod to test the live container. It successfully connected and returned a prediction.

Testing the Live Docker Container : ![alt text](<Capture d'écran 2025-11-16 115614.png>)
![alt text](<Capture d'écran 2025-11-16 115722.png>)