

from database.connection import get_connection
import mysql.connector

from database.local_db import logged_in_users_cache


def get_max_soldier_shift(bale_id):
    user = get_user_by_bale_id(bale_id)
    if not user:
        return 0
    return user.get("max_shifts", 0)

# ok with mySQL
def get_user_by_bale_id(bale_id):
    cursor = None
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE bale_id = %s LIMIT 1",
            (bale_id,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def get_user_by_auth_code(auth_code):
    cursor = None
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE auth_code = %s LIMIT 1",
            (auth_code,)
        )
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# ok with mySQL
def authenticate_soldier(auth_code, bale_id):
    cursor = None
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT full_name, bale_id FROM users WHERE auth_code = %s", (auth_code,))
        user = cursor.fetchone()

        if user is None:
            return False, "کد احراز هویت نامعتبر است."
        if user["bale_id"] is not None:
            if user["bale_id"] == bale_id:
                return True, f"شما قبلاً احراز هویت شده‌اید {user['full_name']}."
            return False, "این کد قبلاً توسط شخص دیگری فعال شده است!"
        cursor.execute(
            "UPDATE users SET bale_id = %s WHERE auth_code = %s",
            (bale_id, auth_code)
        )
        conn.commit()
        return True, f"خوش آمدید {user['full_name']}! احراز هویت شما با موفقیت انجام شد.\n"
    finally:
        cursor.close()
        conn.close()


# ok with mySQL
def check_authenticate_soldier(bale_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE bale_id = %s LIMIT 1", (bale_id,))
        return cursor.fetchone() is not None
    finally:
        conn.close()




def add_shift(auth_code, day):
    cursor = None
    if not (1 <= day <= 31):
        return False, "روز نامعتبر است (باید بین ۱ و ۳۱ باشد)."

    conn = get_connection()
    conn.autocommit = False
    try:
        cursor = conn.cursor()
        if get_max_soldier_shift(auth_code):
            conn.rollback()
            return False, "شما تمام شیفت های خود را ثبت کرده اید"

        cursor.execute("SELECT COUNT(*) FROM shifts WHERE day_number = %s FOR UPDATE", (day,))
        shift_count = cursor.fetchone()[0]
        if shift_count >= 4:
            conn.rollback()
            return False, "ظرفیت شیفت‌های این روز تکمیل شده است (حداکثر ۴ سرباز)."

        cursor.execute(
            "INSERT INTO shifts (auth_code, day_number) VALUES (%s, %s)",
            (auth_code, day)
        )
        conn.commit()
        return True, "رزرو شیفت شما با موفقیت انجام شد."

    except mysql.connector.errors.IntegrityError:
        conn.rollback()
        return False, "شما قبلاً در این روز یک شیفت رزرو کرده‌اید."

    except Exception as e:
        conn.rollback()
        return False, f"خطای ناشناخته رخ داد: {e}"

    finally:
        cursor.close()
        conn.close()


def get_current_user(bale_id):
    if bale_id in logged_in_users_cache:
        return logged_in_users_cache[bale_id]
    user = get_user_by_bale_id(bale_id)
    if user:
        logged_in_users_cache[bale_id] = user
        return user
    return None

