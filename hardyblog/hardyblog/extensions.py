"""
    :author: hardy Liu
    :url: https://github.com/hardyliu
    :copyright: © 2019 Hardy Liu <curage0620@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
csrf = CSRFProtect()
moment = Moment()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from hardyblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user