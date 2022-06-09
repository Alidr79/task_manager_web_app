from flask_login import UserMixin
from . import login_manager
from .db_work import database


class User(UserMixin):
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.authenticated = False

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated


@login_manager.user_loader
def load_user(ticket_number):
    connection = database().get_connection()
    cursor = connection.cursor()
    user = cursor.execute("SELECT * FROM user WHERE user_id = ?", (ticket_number,)).fetchone()
    if user is None:
        return None
    else:
        return User(int(user['user_id']), user['password'])
