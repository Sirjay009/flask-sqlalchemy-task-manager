import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize db without app first


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # Database configuration
    if os.environ.get("DEVELOPMENT") == "True":
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "DB_URL", "sqlite:///taskmanager.db")
    else:
        uri = os.environ.get("DATABASE_URL")
        if uri and uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions with app
    db.init_app(app)

    # Import routes after app creation to avoid circular imports
    from taskmanager import routes
    app.register_blueprint(routes.bp)  # If using blueprints
    return app

# Optional env.py import (must be after create_app to avoid circular imports)


if os.path.exists("env.py"):
    import env  # noqa
