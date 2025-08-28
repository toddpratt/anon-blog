from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from lxml.html.clean import clean_html
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

import models

from extensions import db
from validation import blog_post_request_schema, blog_post_post_request_schema

blog_bp = Blueprint("blog_bp", __name__)


def query_to_blogs(q):
    return [
        {
            "id": blog.id,
            "name": blog.name,
            "description": blog.description,
            "created": blog.created,
            "username": blog.user.username,
        }
        for blog in q
    ]


def query_to_posts(q):
    return [
        {
            "id": post.id,
            "title": post.title,
            "text": post.text,
            "created": post.created,
            "author": post.blog.user.username
        }
        for post in q
    ]


@blog_bp.route("/user/blgos", methods=["GET"])
@jwt_required()
def get_user_blogs():
    q = db.session \
        .query(models.Blog) \
        .filter_by(user_id=current_user.id) \
        .order_by(models.Blog.created.desc())
    blogs = query_to_blogs(q)
    return {
        "status": "success",
        "data": blogs
    }


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
    blogs = query_to_blogs(q)
    return {
        "status": "success",
        "data": blogs
    }


@blog_bp.route("/blogs/<name>", methods=["GET"])
def get_blog_by_name(name: str):
    blog = db.session \
        .query(models.Blog) \
        .filter_by(name=name) \
        .one_or_none()
    return {
        "status": "success",
        "data": {
            "id": blog.id,
            "name": blog.name,
            "description": blog.description,
            "created": blog.created,
            "username": blog.user.username,
            "posts": query_to_posts(blog.posts)
        }
    }


@blog_bp.route("/blogs", methods=["POST"])
@jwt_required()
def post_blog():
    post_data = blog_post_request_schema.load(request.json)
    blog = models.Blog(
        name=post_data["name"],
        description=post_data["description"],
        created=datetime.utcnow(),
        user_id=current_user.id,
    )
    db.session.add(blog)
    try:
        db.session.commit()
    except IntegrityError:
        return {
            "status": "failed"
        }
    return {
        "status": "success",
        "newId": blog.id,
    }


@blog_bp.route("/posts", methods=["GET"])
def get_recent_posts():
    offset = request.args.get("offset")
    q = db.session.query(models.Post) \
        .order_by(models.Post.created.desc()) \
        .limit(10)
    if offset:
        q = q.offset(offset)
    posts = query_to_posts(q)
    return {
        "status": "success",
        "data": posts,
    }


@blog_bp.route("/blogs/<int:blog_id>/posts", methods=["GET"])
def get_posts(blog_id: int):
    q = db.session.query(models.Post) \
        .filter_by(blog_id=blog_id) \
        .order_by(models.Post.created.desc()) \
        .limit(10)
    if request.args.get("offset"):
        q = q.offset(request.args.get("offset"))
    posts = query_to_posts(q)
    return {
        "status": "success",
        "data": posts,
    }


@blog_bp.route("/blogs/<int:blog_id>/posts", methods=["POST"])
@jwt_required()
def post_post(blog_id: int):
    post_data = blog_post_post_request_schema.load(request.json)
    blog = db.session.query(models.Blog).get(blog_id)
    if blog.user_id != current_user.id:
        return {
            "status": "failed",
            "reason": "You do not have access to this blog."
        }, 403

    title = post_data["title"]
    text = clean_html(post_data["text"])

    if not title or not text:
        return {"status": "failed", "reason": "Missing field title or text"}, 400

    post = models.Post(
        blog_id=blog_id,
        title=title,
        text=text,
        created=datetime.utcnow()
    )
    db.session.add(post)
    db.session.commit()
    return {
        "status": "success",
        "newId": post.id,
    }

