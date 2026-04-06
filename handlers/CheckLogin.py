from database.crud import authenticate_soldier,check_authenticate_soldier
from config import users


def authenticate_soldier_test(auth_code, bale_id):

    user = None

    for u in users:
        if auth_code == u["auth_code"]:
            user = u
            break

    if user is None:
        return False, "کد احراز هویت نامعتبر است."

    if user['bale_id'] is not None:
        if user['bale_id'] == bale_id:
            return True, f"شما قبلاً احراز هویت شده‌اید {user['full_name']}."
        else:
            return False, "این کد قبلاً توسط شخص دیگری فعال شده است!"

    user['bale_id'] = bale_id

    return True, f"خوش آمدید {user['full_name']}! احراز هویت شما با موفقیت انجام شد."


def check_authenticate_soldier_test(bale_id):



    for user in users:
        if user["bale_id"] == bale_id:
            return True

    return False

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
