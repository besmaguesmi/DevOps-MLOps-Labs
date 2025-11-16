import os
import pytest
from sklearn.datasets import load_iris
from joblib import load

# Assume train.py saves the model to this path
MODEL_PATH = "models/iris_classifier.pkl"


# Test 1: Check if the model file was created after training
def test_model_file_exists():
    # Ensure you run 'python src/train.py' at least once before testing
    assert os.path.exists(MODEL_PATH), "Model file not found. Run training script first."


# Test 2: Check if the loaded model is a valid scikit-learn estimator
def test_model_loading_and_type():
    if not os.path.exists(MODEL_PATH):
        pytest.skip("Model file not found, skipping type test.")

    model = load(MODEL_PATH)
    assert hasattr(model, 'predict'), "Loaded object is not a valid model (missing .predict)."
    assert hasattr(model, 'coef_'), "Loaded model is missing coefficients."


# [cite_Vstart]Test 3: Check data loading sanity check
def test_data_loading():
    data = load_iris()
    assert data.data.shape == (150, 4)
    assert data.target.shape == (150,)
