import yaml
import psycopg2

with open("CONFIG.yml", "r") as f:
    db_creds = yaml.safe_load(f)

db_config = db_creds["database"]

def get_connection():
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        dbname=db_config["name"],
        user=db_config["user"],
        password=db_config["password"],
        sslmode=db_config["sslmode"]
    )
    return conn