# REPORT
## Running the App

Clone the repository and navigate to the project folder:

```
git clone <your-forked-repo-url>
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

This will train the model and save it to the models/ folder.

Testing the Model

To test the model functionality:
```
pytest tests/test_model.py
```

This runs the unit tests for the IrisClassifier and data loading.

The tests check model initialization, training, prediction, evaluation, and saving/loading functionality.