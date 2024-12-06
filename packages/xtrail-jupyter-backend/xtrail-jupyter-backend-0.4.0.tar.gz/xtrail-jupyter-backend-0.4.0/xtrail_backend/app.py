from flask import Flask, jsonify, request
import os
import uuid
import subprocess
from functools import wraps
from pyngrok import ngrok
import time

app = Flask(__name__)

# Environment-based credentials for security
USERNAME = os.getenv("XTRAIL_USER", "admin")
PASSWORD = os.getenv("XTRAIL_PASS", "7892307634@X")
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN", None)  # Ensure this is set!

# Initialize ngrok with the token
if NGROK_AUTH_TOKEN:
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)


# Authentication decorator
def require_auth(f):
    """Decorator to enforce username/password authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            return jsonify({"message": "Unauthorized access"}), 401
        return f(*args, **kwargs)
    return decorated


# Start Jupyter Notebook server
def start_jupyter(port, token):
    """Start a Jupyter Notebook server."""
    try:
        base_cmd = "jupyter-notebook --no-browser --ip=0.0.0.0 --allow-root"
        cmd = f"{base_cmd} --NotebookApp.token='{token}' --port {port}"
        print(f"Starting Jupyter Notebook on port {port} with token {token}...")
        subprocess.Popen(cmd, shell=True)
        time.sleep(5)  # Give Jupyter time to initialize
    except Exception as e:
        print(f"Error starting Jupyter Notebook: {e}")


# Start ngrok tunnel
def start_ngrok(port):
    """Start an ngrok tunnel for the given port."""
    try:
        url = ngrok.connect(port, bind_tls=True).public_url
        print(f"ngrok Public URL: {url}")
        return url
    except Exception as e:
        print(f"Error starting ngrok: {e}")
        return None


@app.route("/")
def index():
    """Index route."""
    return jsonify({"message": "Welcome to the XTrail Jupyter Backend!"})


@app.route("/start-jupyter", methods=["POST"])
@require_auth
def start_jupyter_endpoint():
    """Start a Jupyter Notebook server and expose it via ngrok."""
    port = 8888
    token = str(uuid.uuid4())

    # Start Jupyter Notebook
    start_jupyter(port, token)

    # Start ngrok
    public_url = start_ngrok(port)
    if not public_url:
        return jsonify({"message": "Failed to start ngrok tunnel"}), 500

    return jsonify({
        "message": "Jupyter Notebook started successfully!",
        "public_url": public_url,
        "token": token
    })


def start_backend():
    """Start the Flask backend with ngrok."""
    print("Starting Flask backend...")
    flask_port = 5000

    # Expose Flask app via ngrok
    flask_url = start_ngrok(flask_port)
    if flask_url:
        print(f"Flask backend is running at: {flask_url}")
    else:
        print("Failed to expose Flask backend via ngrok.")

    # Start Flask app
    app.run(host="0.0.0.0", port=flask_port)


if __name__ == "__main__":
    start_backend()
