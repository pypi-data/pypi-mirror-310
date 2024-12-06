# Utility functions for the backend
import os

def load_environment_vars():
    """Load environment variables for backend credentials."""
    username = os.getenv("XTRAIL_USER", "admin")
    password = os.getenv("XTRAIL_PASS", "7892307634@X")
    NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN", None) 
    return username, password, NGROK_AUTH_TOKEN
