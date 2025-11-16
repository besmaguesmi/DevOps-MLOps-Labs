#!/usr/bin/env python3
"""
Prediction script for Iris classifier - NOW WITH FLASK API
"""

from flask import Flask, request, jsonify

# We need to import our model and data loader
from model import IrisClassifier
from data_loader import get_target_names

# --- Create Flask App ---
app = Flask(__name__)

# --- Load Model Globally ---
# Load the model and target names when the app starts
try:
    classifier = IrisClassifier()
    classifier.load_model('models/iris_classifier.pkl')
    target_names = get_target_names()
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Model not found. Please run train.py first.")
    classifier = None
except Exception as e:
    print(f"Error loading model: {e}")
    classifier = None


# --- Define API Routes ---

@app.route('/')
def home():
    """Home endpoint with API usage info."""
    return jsonify({
        "message": "Welcome to the Iris Classifier API!",
        "usage": "Send a POST request to /predict with JSON data.",
        "example": {
            "features": [5.1, 3.5, 1.4, 0.2]
        }
    })


@app.route('/predict', methods=['POST'])
def predict():
    """Prediction endpoint."""
    if classifier is None:
        return jsonify({"error": "Model is not loaded. Run train.py."}), 500

    if not request.json:
        return jsonify({"error": "No JSON data provided."}), 400

    if 'features' not in request.json:
        return jsonify({"error": "Missing 'features' key in JSON."}), 400

    try:
        # Get features, ensure it's a 2D array for the model
        features = [request.json['features']]

        # Make prediction
        prediction_idx = classifier.predict(features)[0]
        prediction_name = target_names[prediction_idx]

        # Get probabilities
        probabilities = classifier.model.predict_proba(features)[0]
        prob_dict = {
            target_names[i]: prob for i, prob in enumerate(probabilities)
        }

        return jsonify({
            "prediction": int(prediction_idx),
            "class_name": prediction_name,
            "probabilities": prob_dict
        })

    except Exception as e:
        return jsonify({"error": f"Prediction error: {str(e)}"}), 500


# --- Main Function (for running the server) ---

if __name__ == "__main__":
    # This now starts the Flask server
    # host='0.0.0.0' makes it accessible outside the container later
    app.run(debug=True, port=5000, host='0.0.0.0')

    