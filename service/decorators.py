import jwt
from flask import abort, request

from constants import JWT_ALGO, JWT_SECRET


def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        token = request.headers['Authorization']
        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception:
            abort(401)

        res = func(*args, **kwargs)

        return res

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        token = request.headers['Authorization']
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception:
            abort(401)

        if data['role'] != 'admin':
            abort(403)

        res = func(*args, **kwargs)

        return res

    return wrapper
