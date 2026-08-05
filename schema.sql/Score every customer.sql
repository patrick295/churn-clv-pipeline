CREATE OR REPLACE TABLE analytics.customer_predictions AS

SELECT

    customer_id,

    frequency,

    monetary,

    avg_review_score,

    tenure_days,

    analytics.predict_churn(
        frequency,
        monetary,
        avg_review_score,
        tenure_days
    ) AS churn_probability,

    monetary *
    (
        1 -
        analytics.predict_churn(
            frequency,
            monetary,
            avg_review_score,
            tenure_days
        )
    )
    AS predicted_clv,

    CASE

        WHEN analytics.predict_churn(
            frequency,
            monetary,
            avg_review_score,
            tenure_days
        ) >= 0.70

        THEN 'High Risk'

        WHEN analytics.predict_churn(
            frequency,
            monetary,
            avg_review_score,
            tenure_days
        ) >= 0.40

        THEN 'Medium Risk'

        ELSE 'Low Risk'

    END

    AS churn_segment

FROM analytics.customer_features;


SELECT *
FROM analytics.customer_predictions
LIMIT 20;