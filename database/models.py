from database.connection import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name VARCHAR(50) NOT NULL,
        auth_code TEXT UNIQUE NOT NULL,
        bale_id INTEGER UNIQUE,
        role TEXT DEFAULT "soldier"
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day_number INTEGER NOT NULL CHECK(day_number >= 1 AND day_number <= 31),
            auth_code TEXT NOT NULL,
            FOREIGN KEY (auth_code) REFERENCES users (auth_code),
            UNIQUE(auth_code, day_number)
        )
    ''')

    conn.commit()
    conn.close()
