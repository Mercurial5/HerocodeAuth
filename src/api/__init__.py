from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import PostgreSQLConfig, RedisConfig, TokenConfig, EmailConfig


db = SQLAlchemy()
migrate = Migrate()


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(PostgreSQLConfig)
    app.config.from_object(RedisConfig)
    app.config.from_object(TokenConfig)
    app.config.from_object(EmailConfig)

    
    db.init_app(app)
    migrate.init_app(app, db)

    from api.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app