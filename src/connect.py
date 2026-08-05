from snowflake.snowpark import Session
from dotenv import load_dotenv
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

print("Connected successfully!")

print("Account loaded:", os.getenv("SNOWFLAKE_ACCOUNT"))
print("User loaded:", os.getenv("SNOWFLAKE_USER"))


session = Session.builder.configs(connection_params).create()

print("✅ Connected to Snowflake!")
print(session.sql("SELECT CURRENT_USER()").collect())
print(session.sql("SELECT CURRENT_DATABASE()").collect())
print(session.sql("SELECT CURRENT_SCHEMA()").collect())

session.close()
