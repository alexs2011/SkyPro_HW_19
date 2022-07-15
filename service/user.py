import base64
import hashlib
import hmac

from constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, user_id):
        return self.dao.get_one(user_id)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, data):
        data['password'] = self.get_hash(data['password'])
        return self.dao.create(data)

    def update(self, data):
        return self.dao.update(data)

    def delete(self, user_id):
        self.dao.delete(user_id)

    def get_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, new_password, hashed_password):
        return hmac.compare_digest(
            base64.b64decode(hashed_password),
            base64.b64decode(self.get_hash(new_password))
        )
