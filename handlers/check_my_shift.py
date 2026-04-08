from config import CALLBACK_DICTIONOARY as dict
from database.local_db import user_shifts_cache,user_max_shifts_cache
from database.crud import get_current_user
def register(bot):
    @bot.message_handler(func=lambda message:message.text==dict["See My Shifts"])
    def MyStatus(message):
        #check if soldier has set any shift
        user = get_current_user(message.from_user.id)
        if user==None:
            error_text = f"❌ <b>خطا در احراز هویت:</b>\n{response_text}\n\n🔄 لطفاً دوباره تلاش کنید."
            bot.send_message(message.from_user.id, error_text,parse_mode='HTML')
            return
        user_auth_code=get_current_user(message.from_user.id)["auth_code"]
        shifts = user_shifts_cache.get(user_auth_code)
        text= make_message_shift(shifts)
        bot.reply_to(message,text)
        return
def make_message_shift(shifts):
    shift_count = len(shifts)
    if shift_count == 0:
        return "سرباز گرامی، شیفتی برای شما تاکنون ثبت نشده، جهت ثبت شیفت به منو انتخاب شیف مراجعه کنید."
    elif shift_count==1:
        return  f"تنها شیفت شما در تاریخ {shifts[0]}ام ثبت شده است."
    else:
        message = "شیفت های رزرو شده شما در روز های "
        while shift_count > 2:
            message+= f"{shifts[shifts_count-1]}ام ، "
            shift_count -= 1
        message += f"{shifts[shift_count-2]}ام و {shifts[shift_count-1]}ام ثبت شده است."
        return message
