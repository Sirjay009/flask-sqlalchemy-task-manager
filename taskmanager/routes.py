from flask import render_template
from taskmanager import app, db
from taskmanager import Category, Task


@app.route("/")
def home():
    return render_template("base.html")
