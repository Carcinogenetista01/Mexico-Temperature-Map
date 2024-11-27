import streamlit as st
from streamlit_app import main
from flask import Flask, request, jsonify
import threading
import subprocess

flask_app = Flask(__name__)

@flask_app.route('/_ah/warmup')
def warmup():
    # Perform warmup tasks if needed
    return '', 200

def run_streamlit():
    subprocess.run(["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"])

streamlit_thread = threading.Thread(target=run_streamlit)
streamlit_thread.start()

@flask_app.route('/')
def index():
    return jsonify({"message": "Streamlit app is running on port 8501"}), 200

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=8080)