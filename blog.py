from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

import models

from extensions import db


blog_bp = Blueprint("blog_bp", __name__)


@blog_bp.route("/blogs", methods=["GET"])
def get_blogs():
    offset = request.args.get("offset")
    q = db.session \
        .query(models.Blog) \
        .options(joinedload("user")) \
        .order_by(models.Blog.created.desc()) \
        .limit(10)
    if offset:
        q = q.offset(offset)
    blogs = [
        {
            "id": blog.id,
            "name": blog.name,
            "description": blog.description,
            "created": blog.created,
            "username": blog.user.username,
        }
        for blog in q
    ]
    return {
        "status": "success",
        "data": blogs
    }


@blog_bp.route("/blogs", methods=["POST"])
@jwt_required()
def post_blog():
    user_id = get_jwt_identity()
    blog = models.Blog(
        name=request.json.get("name"),
        description=request.json.get("description", ""),
        created=datetime.utcnow(),
        user_id=user_id,
    )
    db.session.add(blog)
    db.session.commit()
    return {
        "status": "success",
        "new_id": blog.id
    }


@blog_bp.route("/blogs/<int:blog_id>/posts", methods=["GET"])
def get_posts(blog_id: int):
    q = db.session.query(models.Post) \
        .filter_by(blog_id=blog_id) \
        .order_by(models.Post.created.desc()) \
        .limit(10)
    if request.args.get("offset"):
        q = q.offset(request.args.get("offset"))
    posts = [
        {
            "id": post.id,
            "title": post.title,
            "text": post.text,
            "created": post.created
        }
        for post in q
    ]
    return {
        "status": "success",
        "data": posts,
    }


@blog_bp.route("/blogs/<int:blog_id>/posts", methods=["POST"])
@jwt_required()
def post_post(blog_id: int):
    post = models.Post(
        blog_id=blog_id,
        title=request.json.get("title"),
        text=request.json.get("text"),
        created=datetime.utcnow()
    )
    db.session.add(post)
    db.session.commit()
    return {
        "status": "success",
        "new_id": post.id,
    }

