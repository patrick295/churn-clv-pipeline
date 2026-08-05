from snowflake.snowpark import Session
from dotenv import load_dotenv
from snowflake.snowpark.functions import col, max as sf_max, min as sf_min, count, sum as sf_sum, avg, datediff, lit
import os

# Load environment variables
load_dotenv()

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

max_date_row = session.table("analytics.customer_order_base").select(sf_max(col("order_date")).alias("max_date")).collect()[0]
dataset_max_date = max_date_row["MAX_DATE"]
print("Using dataset max date as refernce point dataset_max_date:", dataset_max_date)

base = session.table("analytics.customer_order_base")

features =(
    base.group_by("customer_id")
    .agg(
        sf_max(col("order_date")).alias("last_order_date"),
        sf_min(col("order_date")).alias("first_order_date"),
        count(col("order_id")).alias("frequency"),
        sf_sum(col("order_value")).alias("monetary"),
        avg(col("avg_review_score")).alias("avg_review_score"),
        datediff("day",sf_max(col("order_date")),lit(dataset_max_date)).alias("days_since_last_order")
    )
    .with_column("recency_days", datediff("day", col("last_order_date"), lit(dataset_max_date)))
    .with_column("tenure_days", datediff("day", col("first_order_date"), lit(dataset_max_date)))
    .with_column("churned", (col("recency_days")>180).cast("int"))
)

features.write.save_as_table("analytics.customer_features", mode="overwrite")
print("wrote analytics.customer_features:", features.count(), "rows")

session.close()