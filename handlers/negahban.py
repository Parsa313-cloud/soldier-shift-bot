from menu_handlers.calendars import days_status_menu_admin,admin_day_reservations_menu
from utils.decorators import admin_required
from config import ADMIN_DICTIONARY
from core.shift_service import soldier_reservations
from database.db_operations import get_user_by_bale_id




def register(bot):
    @admin_required
    @bot.message_handler(func=lambda message:message.text==ADMIN_DICTIONARY["add_negahban"])
    def add_negahban(message):
        auth_code = "negahban"
        bot.send_message(
                message.chat.id,
                f" شیفت\n\nبرای انتخاب رزرو روی روز مورد نظر خود بزنید. روزهایی که 🔒 را دارند شیفت‌ها در آن روز پر شده است.",
                reply_markup=days_status_menu_admin(auth_code),
        )
    @admin_required
    @bot.message_handler(func=lambda message: message.text in ADMIN_DICTIONARY["remove_negahban"])
    def delete_shift_reserved(message):
        user_data = get_user_by_bale_id(message.chat.id)
        if user_data is None:
            bot.send_message(
                message.chat.id,
                "❌ سرباز عزیز، اطلاعات شما در سیستم یافت نشد. لطفاً ابتدا ثبت‌نام کنید."
            )
        else:
            auth_code = "negahban"
            reservations = soldier_reservations(auth_code)
            if len(reservations)==0:
                bot.send_message(
                    message.chat.id,
                    "⚠️ شما در حال حاضر هیچ شیفتی رزرو نکرده‌اید."
                )
            else:
                markup = admin_day_reservations_menu(reservations,auth_code)
                bot.send_message(
                    message.chat.id,
                    "🗓 **لیست شیفت‌های رزرو شده‌ی :**\n\n👇 لطفاً برای لغو شیفت، روی روز مورد نظر کلیک کنید:",
                    reply_markup=markup,
                    parse_mode="Markdown"
                )


