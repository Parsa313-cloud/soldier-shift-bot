import json
from database.connection import get_connection


user_shifts_cache = {}
day_reservations_cache = {day: [] for day in range(1, 32)}
user_max_shifts_cache = {}
user_names_cache = {}
logged_in_users_cache = {}


def load_data_on_startup():
    conn = None
    cursor = None
    conn = get_connection()
    if not conn:
        print("خطا: اتصال به دیتابیس برقرار نشد.")
        return

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT auth_code, shift, bale_id, max_shifts FROM users WHERE shifts IS NOT NULL")
        all_rows = cursor.fetchall()
        for row in all_rows:
            auth_code = row["auth_code"]
            shifts_data = row["shift"]
            bale_id = row["bale_id"]
            if isinstance(shifts_data, str):
                try:
                    shifts_list = json.loads(shifts_data)
                except json.JSONDecodeError:
                    shifts_list = []
            else:
                shifts_list = shifts_data or []
            user_shifts_cache[auth_code] = shifts_list
            user_max_shifts_cache[auth_code] = row['max_shifts'] or 0
            user_names_cache[auth_code] = row['full_name']
            logged_in_users_cache[bale_id] = row
            for day in shifts_list:
                if day not in day_reservations_cache:
                    day_reservations_cache[day] = []
                day_reservations_cache[day].append(auth_code)

        print(f"موفقیت: اطلاعات {len(all_rows)} کاربر در دیتابیس محلی (کش) بارگذاری شد.")

    except Exception as e:
        print(f"خطا در خواندن اطلاعات دیتابیس: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_user_shifts_in_db(auth_code, new_shifts_list):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        shifts_json = json.dumps(new_shifts_list)
        query = "UPDATE users SET shift = %s WHERE auth_code = %s"
        cursor.execute(query, (shifts_json, auth_code))
        conn.commit()
        return True
    except Exception as e:
        print(f"❌ Database Update Error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

