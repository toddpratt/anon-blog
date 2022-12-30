import os

from flask import Flask
from flask_cors import CORS

from blog import blog_bp

from extensions import db, migrate, jwt, bcrypt
from user import user_bp


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY")

CORS(app, resources={r".*": {"origins": os.getenv('CORS_DOMAIN', '*'), "supports_credentials": True}})

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)

