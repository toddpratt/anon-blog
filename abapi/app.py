import json
import os

from flask import Flask, jsonify
from marshmallow import ValidationError

from blog import blog_bp

from extensions import db, migrate, jwt, bcrypt, cors, api
from models import User
from settings import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from user import user_bp


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config["API_TITLE"] = "anon-blog"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"

cors.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
bcrypt.init_app(app)
api.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    data = {"status": "failed", "errors": e.args}
    response = jsonify(data)
    response.status_code = 400
    return response


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
