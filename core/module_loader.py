
from handlers import CheckLogin,auth,SoldierStatus,CheckMyShift,ShiftChoosing


def load_modules(bot):
    module_lists=[CheckLogin,
                  SoldierStatus,CheckMyShift,ShiftChoosing,



    auth]

    for module in module_lists:
        module.register(bot)