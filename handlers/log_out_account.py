from config import CALLBACK_DICTIONARY
from core.shift_service import log_out_account_service
from database.db_operations import get_user_by_bale_id


def register(bot):
    @bot.message_handler(func=lambda message: message.text in CALLBACK_DICTIONARY["logout_account"])
    def logout_soldier_account(message):
        user = get_user_by_bale_id(message.chat.id)
        if user is None:
            bot.send_message(
                message.chat.id,
                "❌ سرباز عزیز، اطلاعات شما در سیستم یافت نشد!\n"
                "شما اصلاً وارد نشدید که بخواهید خارج بشید. لطفاً اول ثبت‌نام کنید. 🤷‍♂️📝"
            )
            return
        result , message_response = log_out_account_service(message.chat.id)
        bot.send_message(message.chat.id, message_response)
