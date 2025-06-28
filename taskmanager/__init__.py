import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Optional env.py import
if os.path.exists("env.py"):
        import env  # noqa


# Initialize Flask app
app = Flask(__name__)


app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


# Database configuration
if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
         "DB_URL", "sqlite:///taskmanager.db")
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


from taskmanager import routes # noqa
