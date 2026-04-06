from database.connection import get_connection

def create_tables():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(50) NOT NULL,
                auth_code VARCHAR(20) UNIQUE NOT NULL,
                bale_id BIGINT UNIQUE,
                role VARCHAR(20) DEFAULT 'soldier',
                max_shifts INT DEFAULT 0,
                shift Json 
            )
        """)
    finally:
        cursor.close()
        conn.close()
