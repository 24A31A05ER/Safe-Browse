# 🛡️ SafeBrowse: Phishing URL Detector

A Machine Learning-powered web application to detect phishing URLs and protect users from cyber threats.

---

## 🚀 Overview

SafeBrowse analyzes URLs and classifies them as:

- ✅ Safe (Legitimate)
- ⚠️ Dangerous (Phishing)

It combines:
- 🌐 Frontend (HTML, CSS, JavaScript)
- ⚙️ Backend (Flask API)
- 🧠 Machine Learning Model

---

## 🛠️ Project Structure
phishing-detection-project/
│
├── backend/
│ ├── app.py
│ ├── utils.py
│ ├── phishing_model.pkl
│ ├── scaler.pkl (optional)
│ └── requirements.txt
│
├── frontend/
│ ├── index.html
│ ├── login.html
│ ├── style.css
│ ├── script.js
│ └── SafeBrowse.png
│
├── ml_model/
│ ├── train_model.py
│ ├── train_custom.py
│ └── dataset.csv
│
└── README.md


---

## ⚙️ Installation & Setup

### 🔹 1. Clone Repository

```bash
git clone https://github.com/24A31A05ER/Safe-Browse.git
cd phishing-detection-project
