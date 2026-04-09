import mysql.connector

DB_CONFIG = {
    "host": "185.126.10.222",
    "port": 32040,
    "user": "root",
    "password": "glxtBnBUJUKLuv17ap3c",
    "database": "testtib_db",
}

def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
