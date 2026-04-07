from telebot.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton

from database.local_db import user_names_cache


def admin_panel():
    markup = ReplyKeyboardMarkup()
    my_account = KeyboardButton("وضعیت من ℹ️")
    all_shifts = KeyboardButton("مشاهده تمام شیفت ها")
    search_shifts = KeyboardButton("جست و جوی شیفت ها")
    markup.add(my_account, all_shifts, search_shifts)
    return markup

def search_panel():
    markup = InlineKeyboardMarkup()
    search_day = InlineKeyboardButton("شیفت های یک روز" , callback_data="search_day")
    search_soldier = InlineKeyboardButton("شیفت های یک سرباز", callback_data="search_soldier")
    markup.add(search_day, search_soldier)
    return markup

def all_soldier_names():
    markup = InlineKeyboardMarkup()
    for auth_code, full_name in user_names_cache.items():
        markup.add(InlineKeyboardButton(full_name, callback_data=f"soldier_{auth_code}"))
    return markup
