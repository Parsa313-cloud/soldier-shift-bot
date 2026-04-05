from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
def role_keyboard():
    markup = InlineKeyboardMarkup()
    admin = InlineKeyboardButton("ادمین" ,
                                 callback_data="admin")
    soldier = InlineKeyboardButton("سرباز" ,
                                   callback_data="soldier")
    markup.add(admin,soldier)
    return markup