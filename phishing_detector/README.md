# 🛡️ SafeBrowse: Phishing URL Detector

A Machine Learning-powered web application designed to identify malicious phishing URLs and protect users from cyber threats.

## 🚀 Overview
SafeBrowse uses a classification model trained on the **PhiUSIIL Phishing URL Dataset** to analyze URL features and predict whether a link is legitimate or a phishing attempt.

## 🛠️ Project Structure
- **backend/**: Contains the core Flask/Python logic (`app.py`), utility functions (`utils.py`), and saved preprocessing objects like `scaler.pkl`.
- **frontend/**: The user interface files including `index.html`, `login.html`, `style.css`, and `script.js`.
- **ml_model/**: Stores the training scripts (`train_model.py`, `train_custom.py`) and the raw **PhiUSIIL** CSV dataset.
- **phishing_model.pkl**: The trained machine learning "brain" used for real-time predictions (found in both `backend/` and `ml_model/`).
- **requirements.txt**: List of Python libraries needed to run the project.

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd phishing-detector