import pickle
import numpy as np
from sklearn.base import BaseEstimator
from typing import Tuple
from sklearn.feature_extraction.text import TfidfVectorizer


def load_model(model_path: str) -> BaseEstimator:
    """Loads a trained sklearn model from a pickle file."""
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model(r"C:\Users\Dharmi\OneDrive\Desktop\Assignment 3\model.pkl")
vectorizer = load_model(r"C:\Users\Dharmi\OneDrive\Desktop\Assignment 3\tfidf_vectorizer.pkl")


def score(text: str, model: BaseEstimator, threshold: float) -> Tuple[bool, float]:
    """Scores a trained model on the given text.
    
    Args:
        text (str): The input text.
        model (sklearn.estimator): A trained scikit-learn model.
        threshold (float): Decision threshold for classification.
    
    Returns:
        Tuple[bool, float]: A tuple containing the prediction (bool) and propensity (float).
    """
    if not hasattr(model, 'predict_proba'):
        raise ValueError("The provided model does not support probability predictions.")
    
    # Preprocess the text (modify as needed)
    vectorized_text = vectorizer.transform([text]).toarray()  # Replace with actual text vectorization if needed
    
    # Get probability scores
    probabilities = model.predict_proba(vectorized_text)
    
    # Assuming binary classification (second column is positive class probability)
    propensity = probabilities[0][1]
    prediction = propensity >= threshold
    
    return prediction, propensity

#prediction, propensity = score("congratulations you have been selected for a special reward", model, 0.5)
#print(prediction, propensity)