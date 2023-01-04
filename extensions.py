from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from settings import CORS_DOMAIN

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
cors = CORS(resources={
    r".*": {
        "origins": CORS_DOMAIN,
        "supports_credentials": True,
    }
})
