from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, user_id):
        return self.session.query(User).get(user_id)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create(self, data):
        ent = User(**data)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, user_id):
        user = self.get_one(user_id)
        self.session.delete(user)
        self.session.commit()

    def update(self, data):
        user = self.get_one(data.get("id"))

        user.username = data.get("username")
        user.password = data.get("password")
        user.role = data.get("role")

        self.session.add(user)
        self.session.commit()

        return user
