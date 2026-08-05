CREATE OR REPLACE FUNCTION analytics.predict_churn(
    frequency FLOAT,
    monetary FLOAT,
    avg_review_score FLOAT,
    tenure_days FLOAT
)
RETURNS FLOAT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = (
    'scikit-learn',
    'joblib',
    'pandas'
)
IMPORTS = (
    '@analytics.model_stage/churn_model.joblib'
)
HANDLER = 'predict'
AS
$$
import os
import sys
import joblib

def predict(
    frequency,
    monetary,
    avg_review_score,
    tenure_days
):
    import_dir = sys._xoptions["snowflake_import_directory"]

    model = joblib.load(
        os.path.join(
            import_dir,
            "churn_model.joblib"
        )
    )

    probability = model.predict_proba(
        [[
            frequency,
            monetary,
            avg_review_score,
            tenure_days
        ]]
    )[0][1]

    return float(probability)
$$;


SELECT analytics.predict_churn(3,300,4.7,500);