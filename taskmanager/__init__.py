import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize db without app first


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # Database configuration
    if os.environ.get("FLASK_ENV") == "development":
        # Development configuration
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "DB_URL", "sqlite:///taskmanager.db")
    else:
        # Production configuration
        uri = os.environ.get("DATABASE_URL")
        if not uri:
            raise RuntimeError(
                "DATABASE_URL environment variable not set in production!")        
        # Handle Heroku's postgres:// scheme
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)           
        app.config["SQLALCHEMY_DATABASE_URI"] = uri

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions with app
    db.init_app(app)

    # Import routes after app creation to avoid circular imports
    from taskmanager import routes
    app.register_blueprint(routes.bp)  # If using blueprints
    register_shell_context(app)
    return app


def register_shell_context(app):
    from taskmanager.models import Category, Task

    def shell_context():
        return {'db': db, 'Category': Category, 'Task': Task}
    app.shell_context_processor(shell_context)


# Optional env.py import (must be after create_app to avoid circular imports)


if os.path.exists("env.py"):
    import env  # noqa
