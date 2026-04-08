from config import CALLBACK_DICTIONARY
from database.local_db import user_shifts_cache
from database.crud import get_current_user
def register(bot):
    @bot.message_handler(func=lambda message: message.text == CALLBACK_DICTIONARY["See My Shifts"])
    def my_status(message):
        #check if soldier has set any shift
        user = get_current_user(message.from_user.id)
        if user is None:
            error_text = f"❌ <b>خطا در احراز هویت:</b>🔄 لطفاً دوباره تلاش کنید."
            bot.send_message(message.from_user.id, error_text,parse_mode='HTML')
            return
        user_auth_code=user["auth_code"]
        shifts = user_shifts_cache.get(user_auth_code)
        text= make_message_shift(shifts)
        bot.reply_to(message,text)
        return
def make_message_shift(shifts):
    if not shifts:
        return "سرباز گرامی، تاکنون شیفتی برای شما ثبت نشده است. برای ثبت شیفت به منوی «انتخاب شیفت» مراجعه کنید."
    shifts = sorted(set(shifts))
    if len(shifts) == 1:
        return f"تنها شیفت شما در تاریخ {shifts[0]}ام ثبت شده است."
    if len(shifts) == 2:
        return f"شیفت‌های شما در تاریخ {shifts[0]}ام و {shifts[1]}ام ثبت شده است."
    days_text = "، ".join(f"{d}ام" for d in shifts[:-1])
    days_text += f" و {shifts[-1]}ام"
    return f"شیفت‌های رزرو شده شما در روزهای {days_text} ثبت شده است."

