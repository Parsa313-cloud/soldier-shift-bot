
def register(bot):
    @bot.message_handler(func=func,content_types=[
    "text",
    "photo",
    "video",
    "document",
    "audio",
    "voice",
    "video_note",
    "animation",
    "sticker",
    "location",
    "contact",
    "venue",
    "dice",
    "poll"])
    def login(message):
        bot.send_message(chat_id=message.chat.id, text="""درود و وقت بخیر
لطفا ابتدا جهت استفاده از امکانات ربات، لاگین کنید.
جهت لاگین کدشناسایی خود را وارد و ارسال کنید. (جهت امنیت بیشتر پس از ارسال کد خود را از صفحه چت پاک کنید.)""")
        bot.register_next_step_handler(message, ask_auth_code, bot)


def ask_auth_code(message,bot):
    status,text_respone=authenticate_soldier_test(message.text, message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=text_respone)
    if status == False:
        bot.register_next_step_handler(message, ask_auth_code, bot)


def func(message):
    return not check_authenticate_soldier_test(message.chat.id)
