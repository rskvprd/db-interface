from flask import Blueprint
from flask_login import LoginManager, UserMixin


authorisation = Blueprint('authorisation', __name__, template_folder='templates')
login_manager = LoginManager()


@authorisation.route('/')
def authorise():
    return 'login page'


@login_manager.user_loader
def load_user(user_id):
    return User()


class User(UserMixin):
    def __init__(self, login=None, password_hash=None):
        self.password_hash = password_hash
        self.login = login

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(1)

