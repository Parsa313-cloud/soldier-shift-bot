import mysql.connector

DB_CONFIG = {
    "host": "test-snf-service",
    "user": "root",
    "password": "pDmH2EOJldn3yuLgNs5t",
    "database": "usermgl_db",
}

def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
