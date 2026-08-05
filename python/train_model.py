import os
from pathlib import Path

import pandas as pd
import joblib

from dotenv import load_dotenv

from snowflake.snowpark import Session

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score,
    classification_report,
)


# Load Environment Variables


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

print("=" * 60)
print("Loading Snowflake Credentials...")
print("=" * 60)


# Create Snowflake Session


connection_params = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
}

session = Session.builder.configs(connection_params).create()

print("✅ Connected to Snowflake")

print("\nCurrent User:")
print(session.sql("SELECT CURRENT_USER()").collect())

print("\nCurrent Database:")
print(session.sql("SELECT CURRENT_DATABASE()").collect())

print("\nCurrent Schema:")
print(session.sql("SELECT CURRENT_SCHEMA()").collect())


# Load Feature Table


print("\nLoading analytics.customer_features...")

df = session.table("analytics.customer_features").to_pandas()

print("Dataset Loaded Successfully!")


# Inspect Dataset


print("\nDataset Shape")
print(df.shape)

print("\nFirst Five Rows")
print(df.head())

print("\nDataset Information")
print(df.info())

print("\nSummary Statistics")
print(df.describe())


# Check Class Balance


print("\nCustomer Churn Count")
print(df["CHURNED"].value_counts())

print("\nCustomer Churn Percentage")
print(df["CHURNED"].value_counts(normalize=True))


#  Select Features


X = df[
    [
        "FREQUENCY",
        "MONETARY",
        "AVG_REVIEW_SCORE",
        "TENURE_DAYS",
    ]
].fillna(0)


# Target Variable


y = df["CHURNED"]


# Train/Test Split


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print("\nTraining Rows :", len(X_train))
print("Testing Rows  :", len(X_test))


# Train Random Forest Model


print("\nTraining Random Forest Model...")

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    random_state=42,
)

model.fit(X_train, y_train)

print("Model Training Complete!")


# Predict Probabilities


pred_probs = model.predict_proba(X_test)[:, 1]


# Calculate AUC


auc = roc_auc_score(y_test, pred_probs)

print("\nROC AUC Score")
print(auc)


#  Classification Report


predictions = model.predict(X_test)

print("\nClassification Report")
print(classification_report(y_test, predictions))

# Feature Importance


importance = pd.DataFrame(
    {
        "Feature": X.columns,
        "Importance": model.feature_importances_,
    }
)

importance = importance.sort_values(
    by="Importance",
    ascending=False,
)

print("\nFeature Importance")
print(importance)


#  Save Model


os.makedirs("models", exist_ok=True)

model_path = "models/churn_model.joblib"

joblib.dump(model, model_path)

print(f"\nModel saved successfully to: {model_path}")


# SVerify Saved Model


loaded_model = joblib.load(model_path)

print("\nSaved Model Type")
print(type(loaded_model))


#Close Snowflake Session


session.close()

print("\nSnowflake Session Closed Successfully")

print("\nPipeline Completed Successfully!")
print("=" * 60)