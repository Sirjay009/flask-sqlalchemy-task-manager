import os
from taskmanager import create_app  # Import the factory function

app = create_app()  # Create the app instance

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=os.environ.get("DEBUG", "False") == "True")
