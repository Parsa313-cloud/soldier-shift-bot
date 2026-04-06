from database.crud import get_user_by_bale_id
from utils.decorators import admin_required


def admin_handler(bot):
    @bot.message_handler(func=lambda message: message.text in ["my_account" , "all_shifts" , "search_shifts"])
    @admin_required
    def register(message):
        if message.text == "my_account":
            user = get_user_by_bale_id(message.from_user.id)
            bot.send_message(message.chat.id,
                             f"نام : {user.full_name}\nکد احراز هویت : {user.auth_code}")
        if message.text == "all_shifts":
            # send Exel of shifts
            pass
        if message.text == "search_shifts":
            # we can see shifts of the specific soldier
            # we can see which shifts were booked by which soldiers in a specific day
            pass
