from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import PostgreSQLConfig


app = Flask(__name__)
app.config.from_object(PostgreSQLConfig)

db = SQLAlchemy()
migrate = Migrate(app, db)


def create_app() -> Flask:
    db.init_app(app)
    
    return app