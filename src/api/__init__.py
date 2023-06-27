from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import PostgreSQLConfig, RedisConfig, TokenConfig, EmailConfig


db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
mail: Mail = Mail()


def create_app() -> Flask:

    app: Flask = Flask(__name__)

    app.config.from_object(PostgreSQLConfig)
    app.config.from_object(RedisConfig)
    app.config.from_object(TokenConfig)
    app.config.from_object(EmailConfig)
    
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from api.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app