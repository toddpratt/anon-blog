import os

from flask import Flask

from blog import blog_bp

from extensions import db, migrate, jwt, bcrypt, cors
from models import User
from settings import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from user import user_bp


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['JWT_SECRET_KEY'] = SECRET_KEY

cors.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
