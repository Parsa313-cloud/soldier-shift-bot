import mysql.connector

DB_CONFIG = {
    "host": "remote-asiatech.runflare.com",
    "port": 32122,
    "user": "root",
    "password": "pDmH2EOJldn3yuLgNs5t",
    "database": "testgwz_db",
}


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        raise