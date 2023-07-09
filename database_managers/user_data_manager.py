from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data['id']
        self.name = user_data['name']
        self.password = user_data['password']

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
