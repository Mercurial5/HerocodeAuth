from flask import Flask
from config import PostgreSQLConfig


app = Flask(__name__)
app.config.from_object(PostgreSQLConfig)

def create_app() -> Flask:

    return app