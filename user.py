from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    unset_jwt_cookies, unset_access_cookies, unset_refresh_cookies
from sqlalchemy.exc import IntegrityError

import models
from extensions import db, bcrypt
from recaptcha import verify
from settings import RECAPTCHA_SECRET

user_bp = Blueprint('user_bp', __name__)


@user_bp.route("/users", methods=["POST"])
def post_user():
    recaptcha_response = request.json.get("recaptcha")
    if not verify(RECAPTCHA_SECRET, recaptcha_response):
        return {"status": "recaptcha-failed"}
    user = models.User(
        username=request.json.get("username"),
        password=bcrypt.generate_password_hash(request.json.get("password"))
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return {"status": "failed"}
    return {"status": "success", "newId": user.id}


@user_bp.route("/login", methods=["POST"])
def post_login():
    username = request.json["username"]
    password = request.json["password"]
    user = db.session.query(models.User).filter_by(username=username).one_or_none()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        resp = jsonify({"status": "success", "token": access_token})
        return resp
    return {"status": "failed"}


@user_bp.route("/logout", methods=["DELETE"])
def delete_login():
    resp = jsonify({'success': True})
    unset_jwt_cookies(resp)
    unset_access_cookies(resp)
    unset_refresh_cookies(resp)
    return resp, 200
