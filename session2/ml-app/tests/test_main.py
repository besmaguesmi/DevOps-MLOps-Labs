import sys
import os
import numpy as np
from src.data_loader import load_iris_data
from src.model import IrisClassifier

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))


class TestIrisClassifier:
    def setup_method(self):
        """Setup method that runs before each test"""
        self.X_train, self.X_test, self.y_train, self.y_test = load_iris_data(
            test_size=0.3,
            random_state=42)
        self.classifier = IrisClassifier()

    def test_model_training(self):
        """Test model training functionality"""
        self.classifier.train(self.X_train, self.y_train)
        assert self.classifier.is_trained

    def test_model_prediction(self):
        """Test model prediction functionality"""
        self.classifier.train(self.X_train, self.y_train)
        predictions = self.classifier.predict(self.X_test[:5])
        assert len(predictions) == 5
        assert all(isinstance(pred, (np.int32, np.int64, int))
                   for pred in predictions)


def test_data_loading():
    """Test data loading function"""
    X_train, X_test, y_train, y_test = load_iris_data()
    assert X_train.shape[0] > 0
    assert X_test.shape[0] > 0
    assert X_train.shape[1] == 4  # 4 features
    assert len(np.unique(y_train)) > 1  # More than one class
