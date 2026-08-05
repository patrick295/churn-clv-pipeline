import os
from pathlib import Path

from dotenv import load_dotenv

from snowflake.snowpark import Session


# Load Environment Variables


env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


# Create Session


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

print("Connected to Snowflake")


# Upload Model


session.file.put(
    "models/churn_model.joblib",
    "@analytics.model_stage",
    auto_compress=False,
    overwrite=True
)

print("Model uploaded successfully!")

session.close()