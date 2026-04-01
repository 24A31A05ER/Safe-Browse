from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
from utils import extract_features

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL & SCALER
# =========================
try:
    model_path = os.path.join(os.path.dirname(__file__), "phishing_model.pkl")
    scaler_path = os.path.join(os.path.dirname(__file__), "scaler.pkl")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
        
    print("[SUCCESS] Model and Scaler loaded successfully")
except Exception as e:
    model = None
    scaler = None
    print(f"[ERROR] Error loading model/scaler: {e}")

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return "Backend with ML is running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "No URL provided"}), 400

    url = data["url"]

    # =========================
    # FEATURE EXTRACTION
    # =========================
    features = extract_features(url)

    # =========================
    # PREDICTION
    # =========================
    if model and scaler:
        scaled_features = scaler.transform(features)
        prediction = model.predict(scaled_features)[0]
        
        # Get probability. train_model output: 1 = SAFE, 0 = DANGEROUS
        # The classes are [0, 1]. The index 1 corresponds to probability of "SAFE".
        probs = model.predict_proba(scaled_features)[0]
        # The class names might not always be [0, 1] ordered if one class is missing,
        # but the classes_ attribute confirms the order.
        # usually 0 index is 0, 1 index is 1.
        class_idx = list(model.classes_).index(1) if 1 in model.classes_ else -1
        if class_idx != -1:
            trust_score = round(probs[class_idx] * 100)
        else:
            trust_score = 0
            
        
        import difflib
        from urllib.parse import urlparse
        
        hostname = urlparse(url).hostname or ""
        has_dot = "." in hostname
        
        popular_domains = ["google.com", "youtube.com", "facebook.com", "instagram.com", "twitter.com", "linkedin.com", "github.com", "amazon.com", "microsoft.com", ".google/"]
        
        is_popular = False
        is_typo = False
        potential_original = ""
        
        # Check for exact matches
        for d in popular_domains:
            if d in hostname:
                is_popular = True
                break
        
        # If not an exact popular domain, check for typosquatting (similarity > 0.8)
        if not is_popular and hostname:
            for d in popular_domains:
                if d.startswith(".") : continue # Skip TLDs for typo check
                ratio = difflib.SequenceMatcher(None, hostname, d).ratio()
                if ratio > 0.8:
                    is_typo = True
                    potential_original = d
                    break

        has_suspicious = any(word in url.lower() for word in ["login", "bank", "verify", "secure", "update", "account"])
        
        if is_popular and not has_suspicious:
            safe = True
            trust_score = max(trust_score, 99)
        elif is_typo:
            safe = False
            trust_score = min(trust_score, 10)
        elif has_dot and not has_suspicious and "https" in url:
            # If it has a valid domain look, is HTTPS and has no bad words, it's very likely safe
            trust_score = max(trust_score, 85)
            safe = True
        else:
            safe = True if trust_score >= 50 else False
            
        warning = f"Possible typosquatting of '{potential_original}'" if is_typo else ""
        
    else:
        # fallback (if model not loaded)
        safe = True
        trust_score = 50
        warning = ""

    return jsonify({
        "safe": safe,
        "trust_score": trust_score,
        "warning": warning
    })

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)