from database.connection import get_connection
import sqlite3

def get_user_by_bale_id(bale_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE bale_id = ?", (bale_id,))
        user = cursor.fetchone()

        if user is not None:
            return True , user
        else:
            return False , None
    finally:
        conn.close()

def authenticate_soldier(auth_code , bale_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE auth_code = ?", (auth_code,))
        user = cursor.fetchone()
        if user is None:
            return False , "کد احراز هویت نامعتبر است."
        if user['bale_id'] is not None:
            if user['bale_id'] == bale_id:
                return True ,  f"شما قبلاً احراز هویت شده‌اید {user['full_name']}."
            else:
                return False ,  "این کد قبلاً توسط شخص دیگری (با اکانت دیگری) فعال شده است!"
        cursor.execute(
            "UPDATE users SET bale_id = ? WHERE auth_code = ?",
            (bale_id, auth_code)
        )
        conn.commit()
        return True , f"خوش آمدید {user['full_name']}! احراز هویت شما با موفقیت انجام شد."
    finally:
        conn.close()


def add_shift(auth_code, day):
    if is_day_full(day):
        return False, "ظرفیت شیفت‌های این روز تکمیل شده است (حداکثر ۴ سرباز)."

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO shifts (auth_code, day_number) VALUES (?, ?)", (auth_code, day))
        conn.commit()
        return True, "رزرو شیفت شما با موفقیت انجام شد."

    except sqlite3.IntegrityError:
        return False, "شما قبلاً در این روز یک شیفت رزرو کرده‌اید."

    except Exception as e:
        return False, f"خطای ناشناخته رخ داد: {e}"

    finally:
        conn.close()


def is_day_full(day_number):
    shift_count = get_shift_count_for_day(day_number)
    return shift_count >= 4


def get_shift_count_for_day(day):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM shifts WHERE day_number = ?", (day,))
        shift_count = cursor.fetchone()[0]
        return shift_count
    finally:
        conn.close()


def get_shift_count_for_user(auth_code):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM shifts WHERE auth_code = ?", (auth_code,))
        shift_count = cursor.fetchone()[0]
        return shift_count
    finally:
        conn.close()
