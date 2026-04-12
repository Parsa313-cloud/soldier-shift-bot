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
            ("علی افشاری", "008500", "admin", 0),
            ("محمد بهرامیان", "12419", "soldier", 3),
            ("پویا هارونی", "2207", "soldier", 4),
            ("علی عبدالهی", "17530", "soldier", 4),
            ("فردین حیدری", "21107", "soldier", 5),
            ("متین علیخانی", "29999", "soldier", 4),
            ("متین باقری", "29110", "soldier", 4),
            ("عرفان قنواتی", "15732", "soldier", 4),
            ("سینا کرمی", "12959", "soldier", 4),
            ("مهدی کرمی", "76580", "soldier", 4),
            ("سینا شجاعی", "12100", "soldier", 4),
            ("پویا ایدر", "08590", "soldier", 4),
            ("محمدرضا قنبری", "11190", "soldier", 4),
            ("محمد مهدی تقوی", "11119", "soldier", 4),
            ("مهدی رضایی", "02006", "soldier", 4),
            ("علی معصوم زاده", "001144", "soldier", 4),
            ("نگهبان", "negahban", "soldier", 200),
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
