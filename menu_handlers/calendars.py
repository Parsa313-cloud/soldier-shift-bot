from core.shift_service import is_day_full
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.local_db import user_shifts_cache,logged_in_users_cache
from core.bot_instant import logger
def days_status_menu(bale_id):
    markup = InlineKeyboardMarkup(row_width=5)
    buttons = []
    for day in range(1, 32):
        if not is_day_full(day):
            btn_text = f"{day}"
        else:
            btn_text = f"🔒 {day}"
        btn_callback = f"day_{day}"
        auth_code = logged_in_users_cache[bale_id].get("auth_code")
        if int(day) in user_shifts_cache.get(auth_code):
            btn_text+="✅"
        buttons.append(InlineKeyboardButton(text=btn_text, callback_data=btn_callback))

    markup.add(*buttons)
    return markup


def day_reservations_menu(days):
    markup = InlineKeyboardMarkup()
    for day in days:
        markup.add(InlineKeyboardButton(f"روز {day}", callback_data=f"delete_{day}"))
    return markup

