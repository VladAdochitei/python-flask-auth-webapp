from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize SQLAlchemy so it can be used in the Models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'iuhjkl123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # login manager 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of tour user table, we are going to use it to query for the user
        return User.query.get(int(user_id))

    # Blueprints for auth routes in the app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprints for non-auth parts of the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app