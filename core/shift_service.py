import threading

from config import MAX_CAPACITY_PER_DAY
from database.local_db import day_reservations_cache, user_shifts_cache, update_user_shifts_in_db, \
    user_max_shifts_cache

shift_lock = threading.Lock()

def is_day_full(day):
    if day_reservations_cache.get(day):
        return len(day_reservations_cache[day]) >= MAX_CAPACITY_PER_DAY
    else:
        return False


def get_day_reservations(day):
    return day_reservations_cache.get(day, [])

def soldier_reservations(auth_code):
    shifts = user_shifts_cache.get(auth_code, [])
    return shifts


def reserve_shift_for_soldier(auth_code, day):
    with shift_lock:
        max_allowed = user_max_shifts_cache.get(auth_code, 0)
        user_shifts = user_shifts_cache.get(auth_code, [])
        if len(user_shifts) >= max_allowed:
            return False, f"⚠️ سقف شیفت‌های شما در این ماه ({max_allowed} شیفت) پر شده است."

        if is_day_full(day):
            return False, "❌ ظرفیت این روز تکمیل شده است."

        current_shifts = user_shifts_cache.get(auth_code, [])
        if day in current_shifts:
            return False, "⚠️ شما قبلاً این روز را رزرو کرده‌اید."

        new_shifts = current_shifts.copy()
        new_shifts.append(day)

        db_success = update_user_shifts_in_db(auth_code, new_shifts)

        if db_success:
            user_shifts_cache[auth_code] = new_shifts

            if day not in day_reservations_cache:
                day_reservations_cache[day] = []
            day_reservations_cache[day].append(auth_code)

            return True, "✅ شیفت شما با موفقیت رزرو شد."
        else:
            return False, "❌ خطای سیستمی! امکان ثبت در دیتابیس وجود ندارد."


def delete_shift_for_soldier(auth_code, day):
    with shift_lock:
        user_shifts = user_shifts_cache.get(auth_code, [])
        if day not in user_shifts:
            return False, "⚠️ شما در این روز شیفتی ندارید."

        new_shifts = user_shifts.copy()
        new_shifts.remove(day)

        db_success = update_user_shifts_in_db(auth_code, new_shifts)
        if db_success:
            user_shifts_cache[auth_code] = new_shifts
            if day in day_reservations_cache and auth_code in day_reservations_cache[day]:
                day_reservations_cache[day].remove(auth_code)
            return True, "✅ شیفت شما با موفقیت لغو شد."
        else:
            return False, "❌ خطای سیستمی! امکان لغو شیفت در حال حاضر وجود ندارد."


