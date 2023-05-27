from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import PostgreSQLConfig


db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(PostgreSQLConfig)
    
    db.init_app(app)
    migrate.init_app(app, db)


    return app