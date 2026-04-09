from config import CALLBACK_DICTIONARY
from core.shift_service import reserve_shift_for_soldier
from database.db_operations import get_user_by_bale_id,get_max_soldier_shift
from menu_handlers.calendars import days_status_menu


def register(bot):
    @bot.message_handler(func=lambda message: message.text == CALLBACK_DICTIONARY["choose shift"])
    def shift_reserve(message):
        max_shifts = get_max_soldier_shift(message.chat.id)

        bot.send_message(
            message.chat.id,
            f"سقف مجاز شما: {max_shifts} شیفت\n\nبرای انتخاب رزرو روی روز مورد نظر خود بزنید. روزهایی که 🔒 را دارند شیفت‌ها در آن روز پر شده است.",
            reply_markup=days_status_menu()
        )
    @bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
    def reserve_day(call):
        user_data = get_user_by_bale_id(call.message.chat.id)
        if not user_data:
            bot.answer_callback_query(call.id, "کاربر یافت نشد!", show_alert=True)
            return

        auth_code = user_data.get("auth_code")
        day = int(call.data.split("_")[1])
        result, response_message = reserve_shift_for_soldier(auth_code, day)
        bot.answer_callback_query(call.id, response_message, show_alert=False)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=response_message,
            reply_markup=days_status_menu(),
            parse_mode='HTML'
        )
