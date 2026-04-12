import mysql.connector

DB_CONFIG = {
    "host": "dbnewsoldier-pcu-service",
    "user": "root",
    "password": "tnQy7tG35bRCwpUoDWri",
    "database": "dbnewsolyqv_db",
}


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Connected Successfully!")
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        raise