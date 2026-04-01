import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
from urllib.parse import urlparse
import shutil
import os

print("Loading dataset...")
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

def extract_features(url):
    try:
        if not isinstance(url, str):
            url = str(url)
        parsed = urlparse(url)
        return [
            len(url),                              # URL length
            1 if parsed.scheme == "https" else 0,  # HTTPS
            url.count("."),                        # dots
            url.count("-"),                        # hyphen count
            url.count("@"),                        # @ symbol
            1 if "login" in url else 0,
            1 if "bank" in url else 0,
            1 if "verify" in url else 0
        ]
    except:
        return [0]*8

print("Extracting 8 custom features from URLs...")
features_list = df["URL"].apply(extract_features).tolist()

X = pd.DataFrame(features_list, columns=["length", "https", "dots", "hyphen", "at", "login", "bank", "verify"])
y = df["label"]

print("Splitting...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Scaling...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

print("Training RF...")
model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
model.fit(X_train_scaled, y_train)

print(f"Accuracy: {model.score(scaler.transform(X_test), y_test)}")

print("Saving model files...")
with open("phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Copying to backend...")
backend_dir = "../backend"
shutil.copy("phishing_model.pkl", os.path.join(backend_dir, "phishing_model.pkl"))
shutil.copy("scaler.pkl", os.path.join(backend_dir, "scaler.pkl"))

print("DONE.")
