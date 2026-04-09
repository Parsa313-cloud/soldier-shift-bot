from database.db_operations import get_current_user, authenticate_soldier
from menu_handlers.admin_menus import admin_panel
from menu_handlers.keyboards_manage import soldier_panel
import html

def register(bot):

    @bot.message_handler(func=lambda message: get_current_user(message.from_user.id) is None)
    def ask_for_login(message):

        text = (
            "👋 *درود و وقت بخیر!*\n\n"
            "🔒 _شما هنوز وارد سیستم نشده‌ا._\n"
            "جهت استفاده از امکانات ربات، لطفاً *کد شناسایی* خود را وارد و ارسال کنید.\n\n"
            "⚠️ *نکته امنیتی:* پیشنهاد می‌کنیم پس از ارسال، کد خود را از صفحه چت پاک کنید."
        )

        msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_auth_code)

    def process_auth_code(message):
        bale_id = message.from_user.id
        auth_code_input = message.text

        result, response_text = authenticate_soldier(auth_code_input, bale_id)

        if result:
            bot.send_message(message.chat.id, f"✅ {response_text}")
            user = get_current_user(bale_id)
            if user:
                check_role(message, user,bot)
        else:
            error_text = (
                f"❌ *خطا در احراز هویت:*\n"
                f"{response_text}\n\n"
                f"🔄 لطفاً دوباره کد معتبر را ارسال کنید."
            )

            msg = bot.send_message(message.chat.id, error_text, parse_mode="Markdown")

            bot.register_next_step_handler(msg, process_auth_code)

def check_role(message, user,bot):
    if user["role"] == "soldier":
        bot.send_message(
                message.chat.id,
                "🛡 <b>سرباز عزیز، خوش آمدید!</b>\n\n🗓 <i>پنل انتخاب شیفت برای شما فعال شد.</i> لطفاً از منوی زیر استفاده کنید:",
                reply_markup=soldier_panel()
            )
    elif user["role"] == "admin":
        bot.send_message(
                message.chat.id,
                "👑 <b>ادمین گرامی، خیلی خوش آمدید!</b>\n\n⚙️ <i>پنل مدیریت سیستم در اختیار شماست.</i>",
                reply_markup=admin_panel(),
                parse_mode="HTML"
            )
