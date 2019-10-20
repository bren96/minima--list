from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uugoazwybaczwi:7c8526f5010e90bf259421da375f1be793ab5a3f8bcead490b0a02437cbca0b3@ec2-54-243-208-234.compute-1.amazonaws.com:5432/da9779rd0a0i19'
    db.init_app(app)

    with app.app_context():
        # Imports
        from . import routes

        # Create tables for our models
        db.create_all()

        return app
