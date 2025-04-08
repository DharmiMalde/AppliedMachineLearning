from flask import Flask, request, jsonify
import pickle
from sklearn.base import BaseEstimator
from score import score, load_model

# Initialize Flask app
app = Flask(__name__)

# Load models
model = load_model(r"C:\Users\Dharmi\OneDrive\Desktop\Assignment 3\model.pkl")
vectorizer = load_model(r"C:\Users\Dharmi\OneDrive\Desktop\Assignment 3\tfidf_vectorizer.pkl")

@app.route('/score', methods=['POST'])
def score_endpoint():
    """Flask endpoint to score the model on the provided text."""
    data = request.get_json()
    
    # Ensure input has a 'text' field
    if 'text' not in data:
        return jsonify({"error": "Text field is required"}), 400
    
    text = data['text']
    threshold = 0.5  # You can change this threshold based on your preference
    
    try:
        prediction, propensity = score(text, model, threshold)
        return jsonify({"prediction": prediction, "propensity": propensity})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
