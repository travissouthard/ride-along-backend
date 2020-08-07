import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

blog = Blueprint("blog", "admin")

@blog.route("/", methods=["GET"])
def get_blog_posts():
    try:
        blogs = [model_to_dict(blog) for blog in models.Blog.select()]
        print(blogs)
        return jsonify(data=blogs, status={"code": 200, "message": "Got the blog posts!"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "There are no blog posts, sorry!"})