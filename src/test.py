from pathlib import Path
import os
from dotenv import load_dotenv
from snowflake.snowpark import session

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
print("Looking for .env at:", env_path, "| exists:", env_path.exists())

print("Account value:", repr(os.getenv("SNOWFLAKE_ACCOUNT")))
print("User value:", repr(os.getenv("SNOWFLAKE_USER")))
print("Password value:", repr(os.getenv("SNOWFLAKE_PASSWORD")))
print("Role value:", repr(os.getenv("SNOWFLAKE_ROLE")))
print("Warehouse value:", repr(os.getenv("SNOWFLAKE_WAREHOUSE")))
print("Database value:", repr(os.getenv("SNOWFLAKE_DATABASE")))
print("Schema value:", repr(os.getenv("SNOWFLAKE_SCHEMA")))


session = Session.builder.configs(connection_params).create()