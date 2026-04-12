from core.shift_service import soldier_reservations
from database.local_db import user_names_cache
from menu_handlers.calendars import days_status_menu, day_reservations_menu
from utils.decorators import admin_required


def register(bot):
    @admin_required
    @bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
    def change_shift(call):
        function = call.data.split("_")[2]
        auth_code = call.data.split("_")[3]
        user_name = user_names_cache.get(auth_code)
        if function == "admin_add_shift":
            bot.send.message(call.message.chat.id , f"پنل شیفت های {user_name} باز شد",
                             reply_markup= days_status_menu(auth_code))

        elif function == "admin_delete_shift":
            reservations = soldier_reservations(auth_code)
            if len(reservations)==0:
                bot.send_message(
                    call.message.chat.id,
                    "⚠️ در حال حاضر هیچ شیفتی رزرو نکرده‌اید."
                )

            else:
                markup = day_reservations_menu(reservations)
                bot.send_message(
                    call.message.chat.id,
                    "🗓 **لیست شیفت‌های رزرو شده‌ی :**\n\n👇 لطفاً برای لغو شیفت، روی روز مورد نظر کلیک کنید:",
                    reply_markup=markup,
                    parse_mode="Markdown"
                )



