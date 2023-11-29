from flask import Flask
from flask_migrate import Migrate
from .models import db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    print("Create App Running - Initialising App and Making Migrations")

    db.init_app(app)
    print("App Iiniatilised")
    migrate = Migrate(app, db)
    print("Migrations Made")

    from fancii.main.routes import main
    from fancii.heroes.routes import heroes

    app.register_blueprint(main)
    app.register_blueprint(heroes, url_prefix='/heroes')

    return app

