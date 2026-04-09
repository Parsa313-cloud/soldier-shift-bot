from handlers.auth_handlers import check_role
from database.db_operations import get_user_by_bale_id
from core.bot_instant import logger
def register(bot):

    @bot.message_handler(commands=['start'])
    def start_command(message):
        user = get_user_by_bale_id(message.from_user.id)

        check_role(message,user,bot)