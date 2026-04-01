"""
=============================================================
  PHISHING URL DETECTOR - MODEL TRAINING SCRIPT
  Dataset: PhiUSIIL_Phishing_URL_Dataset.csv
  Label:  1 = SAFE (Legitimate), 0 = DANGEROUS (Phishing)
=============================================================

HOW TO RUN:
    python train_model.py

OUTPUT FILES CREATED:
    phishing_model.pkl  → trained ML model
    scaler.pkl          → feature scaler
    feature_names.pkl   → list of feature column names
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix
)
import pickle
import os

# ─────────────────────────────────────────────
# STEP 1: Load the dataset
# ─────────────────────────────────────────────
print("=" * 55)
print("  PHISHING DETECTOR - MODEL TRAINING")
print("=" * 55)
print("\n[1/6] Loading dataset...")

CSV_PATH = "PhiUSIIL_Phishing_URL_Dataset.csv"

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"\n❌ Could not find '{CSV_PATH}'\n"
        "   Make sure you placed the CSV file in the same folder as this script.\n"
        "   Extract it from the archive.zip you downloaded from Kaggle."
    )

df = pd.read_csv(CSV_PATH)
print(f"   ✅ Loaded {len(df):,} rows and {len(df.columns)} columns")
print(f"   Label distribution:")
print(f"      SAFE  (1): {(df['label'] == 1).sum():,} rows")
print(f"      PHISH (0): {(df['label'] == 0).sum():,} rows")


# ─────────────────────────────────────────────
# STEP 2: Select features
# ─────────────────────────────────────────────
print("\n[2/6] Selecting features...")

# We drop non-numeric or identifier columns
DROP_COLS = ["FILENAME", "URL", "Domain", "TLD", "Title", "label"]

# All remaining numeric columns are features
FEATURE_COLS = [c for c in df.columns if c not in DROP_COLS]

print(f"   ✅ Using {len(FEATURE_COLS)} features:")
for i, f in enumerate(FEATURE_COLS, 1):
    print(f"      {i:2}. {f}")


# ─────────────────────────────────────────────
# STEP 3: Prepare X and y
# ─────────────────────────────────────────────
print("\n[3/6] Preparing data...")

X = df[FEATURE_COLS].copy()
y = df["label"].copy()

# Fill any missing values with 0
X.fillna(0, inplace=True)

print(f"   ✅ Feature matrix shape: {X.shape}")
print(f"   ✅ Label series shape:   {y.shape}")


# ─────────────────────────────────────────────
# STEP 4: Train / Test Split
# ─────────────────────────────────────────────
print("\n[4/6] Splitting into train/test (80/20)...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print(f"   ✅ Training samples : {len(X_train):,}")
print(f"   ✅ Test samples     : {len(X_test):,}")


# ─────────────────────────────────────────────
# STEP 5: Train the model
# ─────────────────────────────────────────────
print("\n[5/6] Training Random Forest model (this may take ~1-2 minutes)...")

model = RandomForestClassifier(
    n_estimators=100,   # 100 decision trees
    max_depth=20,       # max depth per tree
    random_state=42,
    n_jobs=-1,          # use all CPU cores
    verbose=0
)

model.fit(X_train_scaled, y_train)
print("   ✅ Model training complete!")


# ─────────────────────────────────────────────
# STEP 6: Evaluate & save
# ─────────────────────────────────────────────
print("\n[6/6] Evaluating model...")

y_pred = model.predict(X_test_scaled)
acc    = accuracy_score(y_test, y_pred)

print(f"\n   📊 ACCURACY: {acc * 100:.2f}%\n")
print("   📋 Classification Report:")
print(classification_report(y_test, y_pred,
      target_names=["DANGEROUS (Phishing)", "SAFE (Legitimate)"]))

print("   🔢 Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"      True SAFE  predicted SAFE    : {cm[1][1]:,}")
print(f"      True SAFE  predicted DANGEROUS: {cm[1][0]:,}")
print(f"      True PHISH predicted DANGEROUS: {cm[0][0]:,}")
print(f"      True PHISH predicted SAFE    : {cm[0][1]:,}")

# Feature importance top 10
importances = pd.Series(model.feature_importances_, index=FEATURE_COLS)
top10 = importances.nlargest(10)
print("\n   🏆 Top 10 Important Features:")
for feat, imp in top10.items():
    print(f"      {feat:<35} {imp:.4f}")

# Save everything
print("\n💾 Saving model files...")
with open("phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("   ✅ Saved: phishing_model.pkl")

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
print("   ✅ Saved: scaler.pkl")

with open("feature_names.pkl", "wb") as f:
    pickle.dump(FEATURE_COLS, f)
print("   ✅ Saved: feature_names.pkl")

print("\n" + "=" * 55)
print("  🎉 TRAINING DONE! Model files are ready.")
print("  Now run: python app.py  to start the website")
print("=" * 55)
