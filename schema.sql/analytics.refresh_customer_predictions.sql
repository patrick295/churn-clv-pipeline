CREATE TASK analytics.refresh_customer_predictions
  WAREHOUSE = poe_wh
  SCHEDULE = 'USING CRON 0 5 * * * America/Sao_Paulo'
AS
CREATE OR REPLACE TABLE analytics.customer_predictions AS
SELECT
  customer_unique_id,
  frequency,
  monetary,
  predict_churn(frequency, monetary, avg_review_score, tenure_days) AS churn_probability,
  monetary * (1 - predict_churn(frequency, monetary, avg_review_score, tenure_days)) AS predicted_clv,
  CASE
    WHEN predict_churn(frequency, monetary, avg_review_score, tenure_days) >= 0.7 THEN 'High Risk'
    WHEN predict_churn(frequency, monetary, avg_review_score, tenure_days) >= 0.4 THEN 'Medium Risk'
    ELSE 'Low Risk'
  END AS churn_segment
FROM analytics.customer_features;

ALTER TASK analytics.refresh_customer_predictions RESUME;


SHOW TASKS IN SCHEMA analytics;