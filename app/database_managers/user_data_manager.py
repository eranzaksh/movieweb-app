from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.id
        self.name = user_data.name
        self.password = user_data.password
