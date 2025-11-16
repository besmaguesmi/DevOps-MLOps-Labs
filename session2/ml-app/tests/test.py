import pytest
import numpy as np
from src.data_loader import load_iris_data
from src.model import IrisClassifier

@pytest.fixture
def trained_classifier():
    """Fixture for a trained IrisClassifier"""
    X_train, X_test, y_train, y_test = load_iris_data(test_size=0.3, random_state=42)
    clf = IrisClassifier()
    clf.train(X_train, y_train)
    return clf, X_test, y_test

def test_prediction_shape(trained_classifier):
    """Ensure predictions have the correct shape"""
    clf, X_test, _ = trained_classifier
    preds = clf.predict(X_test)
    assert preds.shape[0] == X_test.shape[0]

def test_prediction_classes(trained_classifier):
    """Ensure predictions only contain valid class labels"""
    clf, X_test, _ = trained_classifier
    preds = clf.predict(X_test)
    valid_classes = {0, 1, 2}
    assert set(preds).issubset(valid_classes)

def test_evaluate_returns_float_and_str(trained_classifier):
    """Ensure evaluate returns accuracy as float and report as string"""
    clf, X_test, y_test = trained_classifier
    accuracy, report = clf.evaluate(X_test, y_test)
    assert isinstance(accuracy, float)
    assert 0 <= accuracy <= 1
    assert isinstance(report, str)
    assert "precision" in report.lower()
