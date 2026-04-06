from database.crud import get_user_by_bale_id
from utils.decorators import soldier_required


def shift_booking(bot):
    @bot.message_handler(commands=['my_shifts' , 'booking shifts' , "my_account"])
    @soldier_required
    def register(message):
        if message.text == "my_shifts":
            pass
        if message.text == "booking shifts":
            pass
        if message.text == "my_account":
            user = get_user_by_bale_id(message.chat.id)
            bot.send_message(
                message.chat.id,
                f"نام شما : {user.full_name}\nکد احراز هویت شما : {user.auth_code} "
            )

