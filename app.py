import os

from flask import Flask

from blog import blog_bp

from extensions import db, migrate, jwt, bcrypt, cors
from settings import SECRET_KEY, SQLALCHEMY_DATABASE_URI
from user import user_bp


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_COOKIE_SECURE'] = True
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = SECRET_KEY


cors.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(blog_bp)

