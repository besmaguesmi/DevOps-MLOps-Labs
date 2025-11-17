<h2>Task 1: Fork the repo</h2>
Description of what I did:

I forked the original instructor's repository to my own GitHub account. This creates a personal copy of the project under my account, allowing me to make changes, push code, and set up my own `GitHub Actions` workflow without affecting the original project.

Proof of execution:
<img src="../screenshot_verification/fork.png">
<img src="../screenshot_verification/fork_2.png">

<h2>Task 2: Setup virtual environment & install packages</h2>
Description of what I did:

1. **Cloned the repo**: I cloned my forked repository to my local machine using `git clone https://github.com/MiiN1136/DevOps-MLOps-Labs-Session2.git`.

2. **Created virtual environment**: I navigated into the project's `session2/ml-app` directory. I then created a local virtual environment named `venv` by running `python -m venv venv`. This isolates the project's dependencies.

3. **Activated environment**: I activated the virtual environment using using powershell, via `.\venv\Scripts\activate` on Windows.

4. **Installed dependencies**: I installed all the required packages for the project using `pip install -r requirements.txt`.

5. **Verified setup**: Finally, I ran the training script with `python src/train.py` to confirm that the environment was set up correctly and the script could run successfully.

Proof of execution:
1. Creating the virtual environment
<img src="../screenshot_verification/venv.png">
2. Running the `train.py` script locally
<img src="../screenshot_verification/train_script.png">

<h2>Task 3: Write unit tests</h2>
Description of what I did:

I confirmed that the project already included a complete set of unit tests in the `test_model.py` file. This file contains 6 meaningful tests that cover the core functionality of the IrisClassifier class and the data_loader module, including:

* test_model_training
* test_model_prediction
* test_data_loading

**Proof of execution:**

I ran the tests locally from my terminal using the pytest src/ command, as required. The screenshot below shows all tests passing successfully.
<img src="../screenshot_verification/tests_confirmed.png"/>

<h2>Task 4: Linting & formatting</h2>
Description of what I did:

I added `flake8` to the project to enforce code style and linting. First, I installed it in the virtual environment using `pip install flake8` and added it to requirements.txt using the command `pip freeze > requirement.txt`.

I then created a `.flake8` configuration file in the project root to set the max-line-length to 88 and to exclude `__init__.py` files from checks.

Finally, I ran the flake8 src/ tests/ command and fixed **all** reported style errors until the command returned no output, ensuring the code meets the style checks.

Proof of execution:
* output before fixing
<img src="../screenshot_verification/flake8.png"/>
* output after fixing
<img src="../screenshot_verification/flake8_after.png">


<h2>Task 5: GitHub Actions CI workflow</h2>
Description of what I did:

I created the necessary folder structure `.github/workflows/` and added a `ci.yml` file. This YAML file defines a CI pipeline that runs on **every push and pull_request** to the main branch, as required.

The workflow file contains a single job, build-and-test, which performs all the required steps:
1. Checkout code: Uses actions/checkout to get the repository code.
2. Set up Python: Uses actions/setup-python to install Python.
3. Install dependencies: Installs all packages from requirements.txt.
4. Run linter: Runs flake8 to check the code style.
5. Run tests: Runs pytest and generates an XML coverage report, which is then uploaded as an artifact using actions/upload-artifact.
6. Build and Upload Docker Image: Builds the Docker image and then saves it as a .tar file, which is uploaded as a run artifact.

Proof of execution:
<img src="../screenshot_verification/push_task_5.png">


<h2>Task 6: Containerise the app</h2>
Description of what I did:

I created a `Dockerfile` in the project's root directory to containerize the application. The Dockerfile uses a `python:3.10-slim` base image, sets a working directory, copies and installs the requirements.txt, and then copies the src directory. Finally, it sets the default command (CMD) to `python src/train.py`, which runs the training script when the container starts.

I verified this locally by first building the image using `docker build -t seance_2_mlapp` . and then running it with `docker run seance_2_mlapp`. The container ran successfully and produced the same output as running the script locally.

Proof of execution:
* Built `Dockerfile`
<img src="../screenshot_verification/dockerfile_2.png">
* Image added to docker desktop:
<img src="../screenshot_verification/docker.png">
* Testing docker image
<img src='../screenshot_verification/run_docker.png'> 
* Pulled most recent repo version
<img src="../screenshot_verification/pulling_repo.png">
* Push latest changes
<img src="../screenshot_verification/push_changes.png">
* Checking and verifying `Actions` tab on GitHub : 
<img src="../screenshot_verification/successful_CI_CD.png">