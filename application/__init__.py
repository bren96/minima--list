from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
    app.config['SECRET_KEY'] = 'blahblah'
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Imports
        from . import routes
        from . import models
        from . import forms

        # Create tables for our models
        db.create_all()

        return app
