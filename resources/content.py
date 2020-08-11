import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

blog = Blueprint("blog", "admin")
video = Blueprint("video", "admin")

@blog.route("/blog", methods=["GET"])
def get_blog_posts():
    try:
        blogs = [model_to_dict(blog) for blog in models.Blog.select()]
        print(blogs)
        return jsonify(data=blogs, status={"code": 200, "message": "Got the blog posts!"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "There are no blog posts, sorry!"})

@blog.route("/blog", methods=["POST"])
def create_blog():
    payload = request.get_json()
    blog = models.Blog.create(**payload)
    blog_dict = model_to_dict(blog)
    return jsonify(data=blog_dict, status={"code": 201, "message": "Successfully made the blog!"})

@video.route("/video", methods=["GET"])
def get_videos():
    try:
        videos = [model_to_dict(video) for video in models.Video.select()]
        print(videos)
        return jsonify(data=videos, status={"code": 200, "message": "Got the videos!"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "There are no videos, sorry!"})

@video.route("/video", methods=["POST"])
def create_video():
    payload = request.get_json()
    video = models.Video.create(**payload)
    video_dict = model_to_dict(video)
    return jsonify(data=video_dict, status={"code": 201, "message": "Successfully made the video!"})