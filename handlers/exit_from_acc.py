
from config import CALLBACK_DICTIONARY as dic


def register(bot):
    @bot.message_handler(lambda message: message.text == dic["خروج از حساب کاربری"])
    def exit_handler(message):
        bot.send_message(message.chat.id,"ok")

