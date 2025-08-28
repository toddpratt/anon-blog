from marshmallow import Schema, fields


class UserPostRequest(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    recaptcha = fields.String(required=True)


class LoginPostRequest(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)


class BlogPostRequest(Schema):
    name = fields.String(required=True)
    description = fields.String(load_default='')


class BlogPostPostRequest(Schema):
    title = fields.String(required=True)
    text = fields.String(required=True)


user_post_request_schema = UserPostRequest()
login_post_request_schema = LoginPostRequest()
blog_post_request_schema = BlogPostRequest()
blog_post_post_request_schema = BlogPostPostRequest()