from database.models import create_tables
from database.connection import get_connection


def populate_database():
    create_tables()
    print("Tables checked/created successfully.")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        if count > 0:
            print("Database is already populated. Skipping insertion.")
            return

        users_to_insert = [
            ("Mohammad Rezaei", "A1X9p", "admin", 0),
            ("Ali Ahmadi", "B2m7K", "soldier", 3),
            ("Hossein Karimi", "C8v3N", "soldier", 4),
            ("Amir Hosseini", "D4q9L", "soldier", 5),
            ("Reza Moradi", "E12tg", "soldier", 3),
            ("Mehdi Jafari", "F5w8R", "soldier", 4),
        ]

        insert_query = """
            INSERT INTO users (full_name, auth_code, role, max_shifts)
            VALUES (%s, %s, %s, %s)
        """

        cursor.executemany(insert_query, users_to_insert)
        conn.commit()

        print(f"Successfully added {cursor.rowcount} users to the database!")

    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    populate_database()
