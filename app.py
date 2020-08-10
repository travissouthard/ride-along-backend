from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

import models
from resources.content import blog
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

CORS(blog, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(blog, url_prefix='/v1/blog')

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/user')

@app.route("/")
def index():
    return "Hi"

if __name__ == "__main__":
    models.initialize()
    app.run(debug=DEBUG, port=PORT)