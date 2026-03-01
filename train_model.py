import pandas as pd
from feature_extraction import extract_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# ---------------------------
# Load Dataset
# ---------------------------
data = pd.read_csv("dataset/urls_dataset.csv")

X = []
y = []

for _, row in data.iterrows():
    X.append(extract_features(row["url"]))

    # Convert -1 → 0 for XGBoost compatibility
    if row["label"] == -1:
        y.append(0)
    else:
        y.append(1)


# ---------------------------
# Train Test Split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# ---------------------------
# Random Forest
# ---------------------------
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)
print("Random Forest Accuracy:", accuracy_score(y_test, rf_pred))

# ---------------------------
# XGBoost
# ---------------------------
xgb = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    eval_metric="logloss",
    use_label_encoder=False
)

xgb.fit(X_train, y_train)

xgb_pred = xgb.predict(X_test)

print("XGBoost Accuracy:", accuracy_score(y_test, xgb_pred))

print("\nXGBoost Classification Report:\n")
print(classification_report(y_test, xgb_pred))

# ---------------------------
# Save Best Model (XGBoost)
# ---------------------------
os.makedirs("model", exist_ok=True)
joblib.dump(xgb, "model/phishing_model.pkl")

print("\nModel saved successfully inside model/ folder.")