import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Optional env.py import
if os.path.exists("env.py"):
        import env  # noqa


app = Flask(__name__)


app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Proper PostgreSQL connection string format:
# postgresql://username:password@localhost:5432/dbname
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


from taskmanager import routes # noqa
