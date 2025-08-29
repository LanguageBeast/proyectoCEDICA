from src.core import entities
from flask import session
from flask import abort
from functools import wraps


def check(permission):
    def decorator(f):
        @wraps(f)
        def wrapper(*arg, **kwargs):
            if not check_permission(session, permission):
                return abort(403)
            return f(*arg, **kwargs)
        return wrapper
    return decorator


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not is_authenticated(session):
            return abort(403)
        return f(*args, **kwargs)
    return wrapper


def is_authenticated(session):
    return session.get("user") is not None


def check_permission(session, permission_name):
    user_email = session.get("user")
    if not user_email:
        return False
    permissions_set = entities.get_permissions(user_email)
    # Verifica si el permiso está presente
    return permission_name in permissions_set
