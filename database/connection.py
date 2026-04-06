import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "your_database_name",
}

def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
