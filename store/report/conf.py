from dotenv import dotenv_values

env_vars = dotenv_values(".env")

DB_HOST = env_vars.get("HOST")
DB_PORT = env_vars.get("PORT")
DB_NAME = env_vars.get("NAME")
DB_USER = env_vars.get("USER")
DB_PASSWORD = env_vars.get("PASSWORD")

USER_ID = env_vars.get("TG_USER_ID")

URI_MONGO = env_vars.get("URI_MONGO")
