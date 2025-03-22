from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# 1. Import CORS
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

# 2. Enable CORS for the entire app
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Register the routes after initializing app and db
from app import routes
