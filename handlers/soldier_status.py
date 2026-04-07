from config import CALLBACK_DICTIONOARY as dict

def register(bot):
    @bot.message_handler(func=lambda message:message.text==dict["My Status"])
    def MyStatus(message):
        bot.send_message(message.chat.id, dict["My Status"])