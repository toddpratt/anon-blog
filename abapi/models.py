from sqlalchemy.orm import relationship

from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime(), nullable=False)

    user = relationship("User")
    posts = relationship("Post")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id', ondelete="CASCADE"))
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime(), nullable=False)

    blog = relationship("Blog", back_populates='posts')

