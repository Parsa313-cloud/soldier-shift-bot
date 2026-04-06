from database.crud import get_user_by_bale_id
from keyboards.keyboards.keyboards_manage import role_keyboard, soldier_panel


def register(bot):
    @bot.message_handler(commands=['start'])
    def register(message):
        user = get_user_by_bale_id(message.from_user.id)
        if user:
            if user["role"] == "soldier":
                bot.send_message(
                    message.chat.id,
                    "پنل انتخاب شیفت برای شما باز شد" ,
                    reply_markup = soldier_panel()
                )
            else:
                bot.send_message(
                    message.chat.id,
                    "خیلی خوش امدی ادمین عزیز" ,
                    reply_markup = admin_panel()
                )
        else:
            bot.send_message(
                message.chat.id,
                "به بات ما خوش آمدید\nنقش خود را انتخاب کنید:",
                reply_markup = role_keyboard()
            )
