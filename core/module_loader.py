
from handlers import check_login,auth,soldier_status,check_my_shift,shift_choosing


def load_modules(bot):
    module_lists=[CheckLogin,
                  SoldierStatus,CheckMyShift,ShiftChoosing,



    auth]

    for module in module_lists:
        module.register(bot)