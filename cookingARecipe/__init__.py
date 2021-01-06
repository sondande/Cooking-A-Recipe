import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(26)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+ os.path.join(basedir, "cAR.db")

    db.init_app(app)

    login_manager = LoginManager()
    #login_view is the name of absolute URL of the view that a person needs to go to for login required sections
    login_manager.login_view="auth.login"
    login_manager.init_app(app)

    from .models import User
    #from .models import Recipes
    #from .models import Ingredients

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from .auth import auth
    app.register_blueprint(auth)

    from .main import main
    app.register_blueprint(main)

    from .profile import profile
    app.register_blueprint(profile)

    return app
