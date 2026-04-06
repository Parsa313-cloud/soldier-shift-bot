from config import users

def get_user_by_bale_id_test(bale_id):

    for user in users:
        if user["bale_id"] == bale_id:
            return user

    return None

def register(bot):
    @bot.message_handler(func=lambda message: True)
    def register(message):
        user = get_user_by_bale_id_test(message.from_user.id)
        if user["role"] == "soldier":
            bot.send_message(
                message.chat.id,
                "پنل انتخاب شیفت برای شما باز شد",
                #reply_markup=soldier_panel()
            )
        else:
            bot.send_message(
                message.chat.id,
                "خیلی خوش امدی ادمین عزیز",
                reply_markup=None
            )


