from flask import Flask, jsonify, request
import os
import uuid
import subprocess
from functools import wraps
from pyngrok import ngrok

app = Flask(__name__)

# Environment-based credentials for security
USERNAME = os.getenv("XTRAIL_USER", "admin")
PASSWORD = os.getenv("XTRAIL_PASS", "7892307634@X")

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            return jsonify({"message": "Unauthorized access"}), 401
        return f(*args, **kwargs)
    return decorated

# Start Jupyter Notebook server
def start_jupyter(port, token):
    base_cmd = "jupyter-notebook --no-browser --ip=0.0.0.0 --allow-root"
    cmd = f"{base_cmd} --NotebookApp.token='{token}' --port {port}"
    subprocess.Popen(cmd, shell=True)

# Start ngrok tunnel
def start_ngrok(port):
    url = ngrok.connect(port, bind_tls=True).public_url
    print(f"Public URL: {url}")
    return url

@app.route("/")
def index():
    return jsonify({"message": "Welcome to the XTrail Jupyter Backend!"})

@app.route("/start-jupyter")
@require_auth
def start_jupyter_endpoint():
    port = 8888
    token = str(uuid.uuid1())
    start_jupyter(port, token)
    public_url = start_ngrok(port)
    return jsonify({
        "message": "Jupyter Notebook started successfully!",
        "public_url": public_url,
        "token": token
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
