from core.shift_service import get_all_shifts, search_day_shift, search_soldier_shift
from database.db_operations import get_user_by_bale_id
from database.local_db import user_names_cache
from menu_handlers.admin_menus import all_soldier_names, search_panel, change_shift
from utils.decorators import admin_required
from config import ADMIN_DICTIONARY
from utils.excel_generator import generate_shifts_excel


def register(bot):
    @admin_required
    @bot.message_handler(func=lambda message: message.text in ADMIN_DICTIONARY.values())
    def admin_handler(message):

        if message.text == ADMIN_DICTIONARY["my_account"]:
            bot.send_chat_action(message.chat.id, 'typing')
            user = get_user_by_bale_id(message.from_user.id)
            bot.send_message(
                message.chat.id,
                f"👤 اطلاعات حساب کاربری شما:\n\n🔸 نام و نام خانوادگی: {user['full_name']}\n🔑 کد احراز هویت: {user['auth_code']}"
            )

        elif message.text == ADMIN_DICTIONARY["all_shifts"]:
            loading_msg = bot.send_message(message.chat.id, "در حال پردازش و دریافت لیست شیفت‌ها... ⏳")
            bot.send_chat_action(message.chat.id, 'typing')

            shift_result = get_all_shifts()
            message_lines = ["📅 لیست کل شیفت‌های رزرو شده در این ماه:\n"]

            for day in range(1, 32):
                names = shift_result.get(day, [])
                if names:
                    names_str = "، ".join(names)
                    message_lines.append(f"🔹 روز {day}: {names_str}")
                else:
                    message_lines.append(f"🔸 روز {day}: --- خالی ---")
            final_message = "\n".join(message_lines)

            bot.edit_message_text(final_message, message.chat.id, loading_msg.message_id)

        elif message.text == ADMIN_DICTIONARY["search_shifts"]:
            bot.send_message(
                message.chat.id,
                "🔍 لطفا نوع جستجوی خود را انتخاب کنید:\n\nشما می‌توانید شیفت‌های یک سرباز خاص را بررسی کنید یا مشاهده کنید در یک روز مشخص چه کسانی شیفت دارند.",
                reply_markup=search_panel()
            )
        elif message.text == ADMIN_DICTIONARY["see_exel"]:
            bot.send_message(
                message.chat.id,"در حال درست کردن فایل اکسل رزرو شیفت ها..." )
            bot.send_chat_action(message.chat.id, 'typing')

            try:
                excel_path = generate_shifts_excel()
                with open(excel_path, 'rb') as excel_file:
                    bot.send_document(
                        message.chat.id,
                        excel_file,
                        caption="📊 فایل اکسل شیفت‌های این ماه خدمت شما."
                    )
            except Exception as e:
                bot.send_message(message.chat.id, "❌ خطایی در تولید فایل اکسل رخ داد.")
                print(f"Excel Export Error: {e}")

    @bot.callback_query_handler(func=lambda call: call.data in ["search_day", "search_soldier"])
    @admin_required
    def search_shifts_handler(call):
        if call.data == "search_day":
            msg = bot.send_message(call.message.chat.id, "📅 لطفا شماره روز مورد نظر خود را وارد کنید (عددی بین ۱ تا ۳۱):")
            bot.register_next_step_handler(msg, search_day_handler)

        elif call.data == "search_soldier":
            loading_msg = bot.send_message(call.message.chat.id, "در حال بارگذاری لیست سربازان... ⏳")
            bot.edit_message_text(
                "👥 لطفا سرباز مورد نظر خود را از لیست زیر انتخاب کنید:",
                chat_id=call.message.chat.id,
                message_id=loading_msg.message_id,
                reply_markup=all_soldier_names()
            )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("soldier_"))
    @admin_required
    def show_soldier_specific_shifts(call):
        loading_msg = bot.send_message(call.message.chat.id, "در حال جستجو در میان شیفت‌ها... ⏳")
        bot.send_chat_action(call.message.chat.id, 'typing')

        auth_code_chosen = call.data.split("_")[1]

        searched_shifts = search_soldier_shift(auth_code_chosen)
        full_name = user_names_cache.get(auth_code_chosen, "ناشناس")

        if searched_shifts:
            searched_shifts.sort()
            days_str = "، ".join(str(day) for day in searched_shifts)
            msg_text = f"👤 شیفت‌های رزرو شده برای **{full_name}**:\n\n🗓 روزهای: {days_str}"
        else:
            msg_text = f"⚠️ سرباز **{full_name}** تا این لحظه هیچ شیفتی در این ماه رزرو نکرده است."

        bot.edit_message_text(msg_text, call.message.chat.id, loading_msg.message_id , reply_markup=change_shift(auth_code_chosen))

    def search_day_handler(message):
        if not message.text or not message.text.isdigit():
            msg = bot.send_message(message.chat.id, "❌ خطا: لطفا فقط یک عدد وارد کنید (مثلاً 15).")
            bot.register_next_step_handler(msg, search_day_handler)

        day_number = int(message.text)
        if day_number < 1 or day_number > 31:
            msg = bot.send_message(message.chat.id, "❌ خطا: روز وارد شده نامعتبر است. لطفا عددی بین ۱ تا ۳۱ وارد کنید.")
            bot.register_next_step_handler(msg, search_day_handler)

        loading_msg = bot.send_message(message.chat.id, "در حال جستجوی شیفت‌های این روز... ⏳")
        bot.send_chat_action(message.chat.id, 'typing')
        names_list = search_day_shift(day_number)

        if names_list:
            names_str = "، ".join(names_list)
            bot.edit_message_text(
                f"✅ لیست افرادی که در روز **{day_number}** شیفت دارند:\n\n👤 {names_str}",
                message.chat.id,
                loading_msg.message_id
            )
        else:
            bot.edit_message_text(
                f"⚠️ در روز **{day_number}** هیچ شیفتی رزرو نشده است و ظرفیت خالی است.",
                message.chat.id,
                loading_msg.message_id
            )