
from handlers import admin,auth_handlers,check_my_shift,delete_shift,shift_choosing,soldier_status,start_command


def load_modules(bot):
    module_lists=[auth_handlers,admin,soldier_status,check_my_shift,delete_shift,shift_choosing,start_command]

    for module in module_lists:
        module.register(bot)