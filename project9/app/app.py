# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, g
from wtf_tinymce import wtf_tinymce
from flask_sqlalchemy_session import flask_scoped_session, current_session
from flask_login import LoginManager, current_user
from database import Base, db_session, init_db
from views import main_route, post_route, user_route, avatar_route, logout_route, profile_route, upload_route, login_route
import config
from models import User

app = Flask(__name__, template_folder='templates', static_folder='upload')
db = flask_scoped_session(db_session, app)
app.config.from_object(config)
init_db()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login_route.login'

@login_manager.user_loader
def get_user(id):
    print('yo!', current_session.query(User).filter(User.id == id).first())
    return current_session.query(User).filter(User.id == id).first()

@app.before_request
def before_request():
    g.user = current_user

__author__ = 'kakoka'

# register

def register_blueprints(app):
    """Register Flask blueprints."""
    bower_blueprint = Blueprint('bower', __name__, static_url_path='', static_folder='bower_components')
    app.register_blueprint(bower_blueprint)
    app.register_blueprint(main_route)
    app.register_blueprint(login_route)
    app.register_blueprint(logout_route)
    app.register_blueprint(post_route)
    app.register_blueprint(user_route)
    app.register_blueprint(avatar_route)
    app.register_blueprint(profile_route)
    app.register_blueprint(upload_route)
    return None

def create_app():
    # login_manager = LoginManager()

    wtf_tinymce.init_app(app)
    register_blueprints(app)
    return app

if __name__ == '__main__':
    # print(get_user(1))
    create_app().run()