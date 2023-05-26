from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import PostgreSQLConfig


app = Flask(__name__)
app.config.from_object(PostgreSQLConfig)

db = SQLAlchemy()

def create_app() -> Flask:
    db.init_app(app)
    
    return app