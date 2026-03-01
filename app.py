from flask import Flask, request, jsonify
import joblib
from feature_extraction import extract_features
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("model/phishing_model.pkl")


# ---------------------------
# Risk Level Logic
# ---------------------------
def get_risk_level(probability):
    if probability >= 0.85:
        return "Low Risk"
    elif 0.60 <= probability < 0.85:
        return "Medium Risk"
    else:
        return "High Risk"


# ---------------------------
# Prediction Endpoint
# ---------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Extract features
    features = extract_features(url)
    features = np.array(features).reshape(1, -1)

    # Get prediction probability
    prob = model.predict_proba(features)[0][1]  # Probability of legit (class 1)
    prediction = model.predict(features)[0]

    result = {
        "url": url,
        "prediction": "Legitimate" if prediction == 1 else "Phishing",
        "probability_legitimate": round(float(prob), 4),
        "risk_level": get_risk_level(prob),
        "block_recommended": True if prob < 0.60 else False
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)