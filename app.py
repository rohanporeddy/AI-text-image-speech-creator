#Python Standard Libraries
import json
import sqlite3
import os


#Third-Party Libraries
import openai
from flask import Flask, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from oauthlib.oauth2 import WebApplicationClient
import requests

#internal imports
from db import init_db_command
from user import User

#Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuraiton"
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)


#OAuth 2 Client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)
#user manager setup
login_manager = LoginManager()
login_manager.init_app(app)

#Native database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    pass


#OAuth 2 client setup
client = WebApplicationClient()



openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        user_value = request.form["user_value"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "assistant", "content": user_value},
                
            ]
        )

        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result") 
    return render_template("index.html", result=result)

#Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

