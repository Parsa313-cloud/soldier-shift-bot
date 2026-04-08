from config import CALLBACK_DICTIONARY
from database.crud import get_user_by_bale_id


def register(bot):
    @bot.message_handler(func=lambda message: message.text == CALLBACK_DICTIONARY["My Status"])
    def my_status(message):
        user = get_user_by_bale_id(message.chat.id)
        if not user:
            bot.send_message(message.chat.id, "❌ <b>خطا:</b> اطلاعات شما در سیستم یافت نشد.", parse_mode='HTML')
            return

        full_name = user["full_name"]
        role = user["role"]
        auth_code = user["auth_code"]
        max_shifts = user["max_shifts"]
        role_fa = "سرباز 🪖" if role == "soldier" else "مدیر 👨🏻‍✈️"
        text = (
            f"👤 <b>جناب {full_name}، وقت بخیر!</b>\n\n"
            f"در اینجا وضعیت فعلی حساب کاربری شما آورده شده است:\n\n"
            f"🔸 <b>نقش شما:</b> {role_fa}\n"
            f"🔸 <b>سقف شیفت‌های مجاز:</b> {max_shifts} شیفت در ماه 🗓\n"
            f"🔸 <b>کد احراز هویت:</b> <code>{auth_code}</code> 🔑\n\n"
            f"<i>💡 نکته: با کلیک روی کد احراز هویت، کد به صورت خودکار کپی می‌شود.</i>"
        )
        bot.send_message(message.chat.id, text, parse_mode='HTML')

