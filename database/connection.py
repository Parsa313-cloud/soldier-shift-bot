import mysql.connector

DB_CONFIG = {
    "host": "user-uhe-service",
    "user": "root",
    "password": "lQnSwiLeF5IKsRtf1b9w",
    "database": "usermgl_db",
}

def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
