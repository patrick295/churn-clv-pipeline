# Customer Churn & Customer Lifetime Value (CLV) Prediction Pipeline

> An end-to-end customer analytics pipeline built with **Snowflake, Snowpark Python, scikit-learn, AWS S3, and Power BI** that predicts customer churn and estimates Customer Lifetime Value (CLV) using the Olist Brazilian E-Commerce dataset.

---

## Project Overview

Understanding which customers are likely to churn—and how valuable they are—is one of the most important use cases in customer analytics.

This project demonstrates how to build a production-style machine learning pipeline using Snowflake as the central analytics platform.

The pipeline:

* Engineers customer behavior features with Snowpark Python
* Trains a churn prediction model using scikit-learn
* Deploys the model into Snowflake using a Python UDF
* Scores customers inside the warehouse
* Automates prediction refreshes with Snowflake Tasks
* Visualizes predictions in Power BI

The project uses the **Olist Brazilian E-Commerce Dataset** from Kaggle.

---

# Architecture

<p align="center">
<img src="docs/architecture.png" width="100%">
</p>

---

# End-to-End Pipeline

```text
Raw Orders
Raw Order Items
Raw Reviews
Raw Customers
        │
        ▼
Order-Level SQL Aggregation
        │
        ▼
Snowpark Python Feature Engineering
        │
        ▼
analytics.customer_features
        │
        ▼
Random Forest Training (scikit-learn)
        │
        ▼
Model saved to Snowflake Stage
        │
        ▼
Python UDF
        │
        ▼
Customer Predictions
        │
        ▼
Snowflake Task
        │
        ▼
Power BI Dashboard
```

---

# Technology Stack

| Category            | Technology      |
| ------------------- | --------------- |
| Cloud Storage       | Amazon S3       |
| Data Warehouse      | Snowflake       |
| Feature Engineering | Snowpark Python |
| Machine Learning    | scikit-learn    |
| Programming         | Python          |
| Data Processing     | Pandas          |
| Model Serialization | Joblib          |
| Scheduling          | Snowflake Tasks |
| Visualization       | Power BI        |

---

# Repository Structure

```text
customer-churn-clv-pipeline/

│
├── sql/
│   ├── 01_customer_orders_base.sql
│   ├── 02_customer_predictions.sql
│   └── 03_refresh_task.sql
│
├── python/
│   ├── connect.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   └── deploy_udf.py
│
├── docs/
│   ├── architecture.png
│   ├── dashboard.png
│   └── pipeline.png
│
├── .env.example
├── requirements.txt
└── README.md
```

---

# Machine Learning Workflow

### 1. Feature Engineering

Customer-level features generated inside Snowflake:

* Recency
* Frequency
* Monetary Value (RFM)
* Customer Tenure
* Average Review Score
* Category Diversity

These features are written back into:

```text
analytics.customer_features
```

---

### 2. Model Training

The feature table is exported to Pandas using Snowpark:

```python
session.table("analytics.customer_features").to_pandas()
```

A Random Forest classifier is trained using scikit-learn.

Model output:

```text
churn_model.joblib
```

---

### 3. Model Deployment

The trained model is uploaded to a Snowflake Stage.

A Python UDF loads the model and performs inference directly inside Snowflake.

Outputs are written to

```text
analytics.customer_predictions
```

---

### 4. Automated Scoring

A Snowflake Task refreshes customer predictions on a schedule.

No external orchestrator is required.

---

# Data Model

### Input Tables

```text
raw.orders

raw.order_items

raw.order_reviews

raw.customers
```

### Output Tables

```text
analytics.customer_features

analytics.customer_predictions
```

---

# Dashboard

The Power BI dashboard includes:

* Total Customers
* High Risk Customers
* Average Predicted CLV
* Churn Probability Distribution
* Customer Segmentation
* High-Value Customers at Risk
* Monetary vs Churn Scatter Plot

<p align="center">
<img src="docs/dashboard.png" width="100%">
</p>

---

# Key Engineering Decisions

### Customer Grain

The Olist dataset contains both:

* `customer_id`
* `customer_unique_id`

`customer_id` represents an order-level identifier, while `customer_unique_id` identifies repeat customers. The pipeline aggregates on `customer_unique_id` to produce meaningful customer-level features.

---

### Churn Definition

The dataset ends in 2018.

Instead of calculating recency relative to the current date, the pipeline uses the dataset's maximum order date as the reference point. This produces more realistic churn labels for a historical dataset.

---

### Why Snowpark?

Snowpark allows feature engineering to run close to the data inside Snowflake, reducing unnecessary data movement. Only the engineered feature table is exported for local model training.

---

# Challenges Encountered

* Configuring AWS IAM trust policies for Snowflake Storage Integrations
* Choosing the correct customer grain (`customer_unique_id`)
* Managing class imbalance caused by historical churn labels
* Deploying a scikit-learn model as a permanent Snowflake Python UDF
* Automating prediction refreshes using Snowflake Tasks

---

# Future Improvements

* Hyperparameter tuning with GridSearchCV
* Experiment tracking with MLflow
* Snowpark ML for in-warehouse model training
* Customer segmentation using clustering
* Model monitoring and drift detection
* Incremental feature generation using Streams

---

# Skills Demonstrated

* Data Engineering
* Snowflake
* Snowpark Python
* Machine Learning
* Feature Engineering
* AWS S3
* SQL
* Python
* Power BI
* MLOps
* Data Modeling
* Customer Analytics

---

# References

* Olist Brazilian E-Commerce Dataset
* Snowflake Documentation
* Snowpark Python Documentation
* scikit-learn Documentation
