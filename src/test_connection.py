from snowflake.snowpark import Session

connection_params = {
    "account": "anchjpk-va30289",
    "user": "PLOGMADE",
    "password": "Justplogit@12345",
    "warehouse": "POE_WH",
    "database": "POE_DB",
    "schema": "ANALYTICS",
    "role": "ACCOUNTADMIN",
}

session = Session.builder.configs(connection_params).create()

print(session.sql("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()").collect())

session.close()