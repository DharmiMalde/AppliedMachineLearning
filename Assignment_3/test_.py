import pickle
import requests
import subprocess
import os
import time
import joblib

from score import score

SAMPLE_MESSAGES = [
]

def load_model():
    """Loads the pre-trained model for testing."""
    with open(r"C:\Users\Dharmi\OneDrive\Desktop\Assignment 3\model.pkl", 'rb') as f:
        model = pickle.load(f)
    return model

def test_score():
    """Tests the score function for correctness and robustness."""
    model = load_model()

    for msg in SAMPLE_MESSAGES:
        # Basic test: Function runs without errors
        result, confidence = score(msg, model, 0.5)
        assert result is not None
        assert confidence is not None

        # Data type checks
        assert isinstance(result, int)
        assert isinstance(confidence, float)

        # Validity checks
        assert 0 <= confidence <= 1  # Confidence must be between 0 and 1
        assert result in [0, 1]  # Result must be either 0 or 1

        # Edge case checks for threshold
        assert score(msg, model, 0.0)[0] == 1  # Threshold 0 should always return 1
        assert score(msg, model, 1.0)[0] == 0  # Threshold 1 should always return 0

    # Testing clear spam and non-spam cases
    assert score("", model, 0.5)[0] == 1  # Spam-like message
    assert score("", model, 0.5)[0] == 0  # Non-spam
    assert score("", model, 0.5)[0] == 1  # Spam
    assert score("", model, 0.5)[0] == 0  # Non-spam

def test_flask():
    """Integration test for verifying the Flask app using localhost."""

    # Kill any process using port 5000
    os.system("fuser -k 5000/tcp" if os.name != "nt" else "netstat -ano | findstr :5000")  # Linux/Mac & Windows

    # Start Flask in a subprocess
    process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for Flask to start
    time.sleep(5)

    
    # Test the home endpoint
    response = requests.get("http://127.0.0.1:5000/")
    assert response.status_code == 200, "Flask app did not start correctly!"

    # Test the classification endpoint
    test_response = requests.post("http://127.0.0.1:5000/classify", data={"message": "Exclusive deal for you!"})
    assert test_response.status_code == 200, "Classification request failed!"

    response_data = test_response.json()
    assert "result" in response_data and "confidence" in response_data, "Invalid response format"
    assert isinstance(response_data["result"], bool), "Result should be boolean"
    assert isinstance(response_data["confidence"], float), "Confidence should be a float"

    # Kill the Flask app process after testing
    os.system("fuser -k 5000/tcp" if os.name != "nt" else "taskkill /F /IM python.exe")