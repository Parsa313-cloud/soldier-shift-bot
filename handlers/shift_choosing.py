from config import CALLBACK_DICTIONARY

def register(bot):
    @bot.message_handler(func=lambda message:message.text==CALLBACK_DICTIONARY["choose shift"])
    def my_status(message):
        bot.send_message(message.chat.id, CALLBACK_DICTIONARY["My Status"])