
from handlers import admin,auth_handlers,check_my_shift,delete_shift,shift_choosing,soldier_status


def load_modules(bot):
    module_lists=[auth_handlers,admin,check_my_shift,delete_shift,shift_choosing,soldier_status]

    for module in module_lists:
        module.register(bot)