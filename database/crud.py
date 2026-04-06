from database.connection import get_connection
import mysql.connector


def get_user_by_bale_id(bale_id):
    cursor = None
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE bale_id = %s", (bale_id,))
        user = cursor.fetchone()

        if user is not None:
            return True, user
        else:
            return False, None
    finally:
        cursor.close()
        conn.close()


def authenticate_soldier(auth_code, bale_id):
    cursor = None
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE auth_code = %s", (auth_code,))
        user = cursor.fetchone()

        if user is None:
            return False, "کد احراز هویت نامعتبر است."

        if user['bale_id'] is not None:
            if user['bale_id'] == bale_id:
                return True, f"شما قبلاً احراز هویت شده‌اید {user['full_name']}."
            else:
                return False, "این کد قبلاً توسط شخص دیگری (با اکانت دیگری) فعال شده است!"

        cursor.execute(
            "UPDATE users SET bale_id = %s WHERE auth_code = %s",
            (bale_id, auth_code)
        )
        conn.commit()
        return True, f"خوش آمدید {user['full_name']}! احراز هویت شما با موفقیت انجام شد."
    finally:
        cursor.close()
        conn.close()


def add_shift(auth_code, day):
    cursor = None
    if not (1 <= day <= 31):
        return False, "روز نامعتبر است (باید بین ۱ و ۳۱ باشد)."

    conn = get_connection()
    conn.autocommit = False
    try:
        cursor = conn.cursor()
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

