from core.shift_service import soldier_reservations
from database.local_db import user_names_cache
from menu_handlers.calendars import days_status_menu_admin, admin_day_reservations_menu
from utils.decorators import admin_required
from core.bot_instant import logger

from core.shift_service import reserve_shift_for_soldier
from database.db_operations import get_user_by_bale_id


def register(bot):
    @admin_required
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
    def change_shift(call):
        function = call.data.split("_")[1]
        auth_code = call.data.split("_")[3]
        user_name = user_names_cache.get(auth_code)
        if function == "add":
            bot.send_message(call.message.chat.id , f"پنل شیفت های {user_name} باز شد",
                             reply_markup= days_status_menu_admin(auth_code))
        elif function == "delete":
            reservations = soldier_reservations(auth_code)
            if len(reservations)==0:
                bot.send_message(
                    call.message.chat.id,
                    "⚠️ در حال حاضر هیچ شیفتی رزرو نکرده‌اید."
                )

            else:
                markup = admin_day_reservations_menu(reservations,auth_code)
                bot.send_message(
                    call.message.chat.id,
                    "🗓 **لیست شیفت‌های رزرو شده‌ی :**\n\n👇 لطفاً برای لغو شیفت، روی روز مورد نظر کلیک کنید:",
                    reply_markup=markup,
                    parse_mode="Markdown"
                )
    @admin_required
    @bot.callback_query_handler(func=lambda call: call.data.startswith("change_day_"))
    def reserve_day(call):
        user_data = get_user_by_bale_id(call.message.chat.id)
        if not user_data:
            bot.answer_callback_query(call.id, "کاربر یافت نشد!", show_alert=True)
            return

        auth_code = call.data.split("_")[3]
        day = int(call.data.split("_")[2])
        result, response_message = reserve_shift_for_soldier(auth_code, day)
        bot.answer_callback_query(call.id, response_message, show_alert=False)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=response_message,
            reply_markup=days_status_menu_admin(auth_code),
            parse_mode="HTML"
        )



