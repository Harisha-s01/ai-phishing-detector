from flask import Flask, request, jsonify
import joblib
from feature_extraction import extract_features
import numpy as np
import socket
from urllib.parse import urlparse

app = Flask(__name__)

# Load trained model
model = joblib.load("model/phishing_model.pkl")


# ---------------------------
# DNS Validation Function
# ---------------------------
def check_dns(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False


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

    parsed_url = urlparse(url)

    # Ignore non-http/https schemes
    if parsed_url.scheme not in ["http", "https"]:
        return jsonify({
            "url": url,
            "prediction": "Unsupported URL",
            "probability_legitimate": None,
            "risk_level": "N/A",
            "block_recommended": False,
            "dns_valid": None
        })

    domain = parsed_url.netloc

    # DNS Validation
    dns_valid = check_dns(domain)

    # Extract ML features
    features = extract_features(url)
    features = np.array(features).reshape(1, -1)

    # ML Prediction
    prob = model.predict_proba(features)[0][1]
    prediction = model.predict(features)[0]

    # Hybrid logic
    if not dns_valid:
        final_prediction = "Phishing"
        prob = prob * 0.5
    else:
        final_prediction = "Legitimate" if prediction == 1 else "Phishing"

    risk_level = get_risk_level(prob)
    block_recommended = True if (final_prediction == "Phishing" or prob < 0.60) else False

    result = {
        "url": url,
        "prediction": final_prediction,
        "probability_legitimate": round(float(prob), 4),
        "risk_level": risk_level,
        "block_recommended": block_recommended,
        "dns_valid": dns_valid
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)