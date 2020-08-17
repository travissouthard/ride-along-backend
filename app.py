import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

import models
from resources.content import blog
from resources.content import video
from resources.content import product
from resources.admin import user

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

CORS(blog, origins=['http://localhost:3000', "https://ridealongpictures.herokuapp.com/"], supports_credentials=True)
app.register_blueprint(blog, url_prefix='/v1/')

CORS(video, origins=['http://localhost:3000', "https://ridealongpictures.herokuapp.com/"], supports_credentials=True)
app.register_blueprint(video, url_prefix='/v1/')

CORS(product, origins=['http://localhost:3000', "https://ridealongpictures.herokuapp.com/"], supports_credentials=True)
app.register_blueprint(product, url_prefix='/v1/')

CORS(user, origins=['http://localhost:3000', "https://ridealongpictures.herokuapp.com/"], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

@app.route("/")
def index():
    return "Visit ridealongpictures.heruko.com to see what this app is for! Or follow us on Instagram at @ridealongpictures or on Twitter at @ridealongpics"

if 'ON_HEROKU' in os.environ: 
    print('\non heroku!')
    models.initialize()

if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT)