import calendar
import datetime

import jwt

from constants import JWT_ALGO, JWT_SECRET
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)
        if not user:
            return False

        if not is_refresh:
            is_password_valid = self.user_service.compare_passwords(password, user.password)
            if not is_password_valid:
                return False

        data = {
            "username": username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        day30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data['exp'] = calendar.timegm(day30.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_refresh_token(self, refresh_token):
        try:
            data = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception:
            return False
        username = data['username']

        user = self.user_service.get_by_username(username)
        if not user:
            return False

        return self.generate_tokens(username, user.password, is_refresh=True)
