import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
if os.path.exists("env.py"):
    import env  # noqa

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Secret Key Configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # Database configuration - STRICT MODE
    uri = os.environ.get("DATABASE_URL")

    if uri:
        # Handle Heroku's postgres:// to postgresql:// conversion
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri
    else:
        # Production safety check
        if os.environ.get("FLASK_ENV") == "production":
            raise ValueError("DATABASE_URL must be set in production!")
        # Fall back to local development DB
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "DB_URL", "sqlite:///taskmanager.db")

    # SQLAlchemy settings
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Connection pooling for production
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 10,
        "max_overflow": 20
    }

    # Development-specific settings
    if os.environ.get("FLASK_ENV") == "development":
        app.config["TEMPLATES_AUTO_RELOAD"] = True
        app.config["SQLALCHEMY_ECHO"] = True  # Show SQL queries

    # Initialize extensions with app
    db.init_app(app)

    # Register Blueprints
    from taskmanager.routes import bp as main_bp
    app.register_blueprint(main_bp)  # If using blueprints

    # Register Shell Context for Flask CLI
    register_shell_context(app)

    return app


def register_shell_context(app):
    from taskmanager.models import Category, Task

    def shell_context():
        return {'db': db, 'Category': Category, 'Task': Task}

    app.shell_context_processor(shell_context)
