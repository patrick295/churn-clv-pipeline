--Customer count by segment

SELECT
   churn_segment,
   COUNT(*)AS customers
FROM analytics.customer_predictions
GROUP BY churn_segment
ORDER BY customers DESC


--Average predicted churn 

SELECT
     ROUND(AVG(churn_probability),3) AS avg_churn_probability
FROM analytics.customer_predictions;

--Average predicted CLV

SELECT
    ROUND(AVG(predicted_clv), 2) AS avg_predicted_clv
FROM analytics.customer_predictions;