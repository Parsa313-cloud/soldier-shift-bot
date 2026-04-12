from config import CALLBACK_DICTIONARY
from core.shift_service import soldier_reservations, delete_shift_for_soldier
from database.db_operations import get_user_by_bale_id
from menu_handlers.calendars import day_reservations_menu


def register(bot):

    @bot.message_handler(func=lambda message: message.text in CALLBACK_DICTIONARY["delete shift"])
    def delete_shift_reserved(message):

        user_data = get_user_by_bale_id(message.chat.id)
        if user_data is None:
            bot.send_message(
                message.chat.id,
                "❌ سرباز عزیز، اطلاعات شما در سیستم یافت نشد. لطفاً ابتدا ثبت‌نام کنید."
            )
        else:
            auth_code = user_data.get("auth_code")
            reservations = soldier_reservations(auth_code)

            if len(reservations)==0:
                bot.send_message(
                    message.chat.id,
                    "⚠️ شما در حال حاضر هیچ شیفتی رزرو نکرده‌اید."
                )

            else:
                markup = day_reservations_menu(reservations)

                bot.send_message(
                    message.chat.id,
                    "🗓 **لیست شیفت‌های رزرو شده‌ی :**\n\n👇 لطفاً برای لغو شیفت، روی روز مورد نظر کلیک کنید:",
                    reply_markup=markup,
                    parse_mode="Markdown"
                )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("delete_"))
    def check_delete_reservation(call):
        day = call.data.split("_")[1]
        user_data = get_user_by_bale_id(call.message.chat.id)

        if not user_data:
            bot.answer_callback_query(call.id, "❌ کاربر یافت نشد!", show_alert=True)
            return

        auth_code = user_data.get("auth_code")
        result, response_message = delete_shift_for_soldier(auth_code, day)
        bot.edit_message_text(
            text=f"✅ {response_message}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
