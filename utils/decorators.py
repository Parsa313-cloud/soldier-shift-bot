from functools import wraps

from database.db_operations import get_user_by_bale_id


def admin_required(func):
    @wraps(func)
    def wrapper(message,*args, **kwargs):
        user = get_user_by_bale_id(message.from_user.id)
        if user["role"] == "admin":
            return func(message,*args, **kwargs)
        else:
            return None
    return wrapper

def soldier_required(func):
    @wraps(func)
    def wrapper(message,*args, **kwargs):
        user = get_user_by_bale_id(message.from_user.id)
        if user["role"] == "soldier":
            return func(message,*args, **kwargs)
        else:
            return None
    return wrapper