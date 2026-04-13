
from handlers import admin,auth_handlers,check_my_shift,delete_shift,shift_choosing,soldier_status,start_command,delete_shift,log_out_account,admin_change_shift, negahban


def load_modules(bot):
    module_lists=[negahban,
        auth_handlers,admin,soldier_status,
        check_my_shift,delete_shift,shift_choosing,
        admin_change_shift,delete_shift,
        log_out_account,start_command
                  ]

    for module in module_lists:
        module.register(bot)