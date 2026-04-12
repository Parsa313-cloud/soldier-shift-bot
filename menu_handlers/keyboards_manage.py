from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def role_keyboard():
    markup = InlineKeyboardMarkup()
    admin = InlineKeyboardButton("ادمین" ,
                                 callback_data="admin")
    soldier = InlineKeyboardButton("سرباز" ,
                                   callback_data="soldier")
    markup.add(admin,soldier)
    return markup

def soldier_panel():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    my_account = KeyboardButton("وضعیت من ℹ️")
    booking_shifts = KeyboardButton("انتخاب شیفت")
    my_shifts = KeyboardButton("مشاهده شیفت های من")
    delete_shift = KeyboardButton("حذف شیفت")
    logout_account = KeyboardButton("خروج از حساب کاربری")
    markup.add(my_account,booking_shifts)
    markup.add(my_shifts,delete_shift , logout_account)
    return markup


