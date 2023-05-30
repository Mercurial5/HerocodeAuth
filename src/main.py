from api import create_app
from api import db
from flask_jwt_extended import JWTManager

app = create_app()
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)