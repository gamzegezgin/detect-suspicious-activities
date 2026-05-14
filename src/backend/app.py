from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os
import sys
import threading
import time
import sqlite3
import hashlib

sys.path.append(os.path.dirname(__file__))
from predict import predict_video

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = 'surveillance-secret-key-2026'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

# ── Database ─────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    ''')
    admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
    c.execute('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)',
              ('admin', admin_pass))
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── Video stream ─────────────────────────────────────────────
VIDEOS_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'videos')
videos = sorted([f for f in os.listdir(VIDEOS_DIR) if f.endswith('.mp4')])

current_index = 0
current_status = {
    "label": "NormalVideos",
    "confidence": 91.0,
    "suspicious": False,
    "video": videos[0] if videos else ""
}

def analyze_next():
    global current_index, current_status
    while True:
        video_name = videos[current_index]
        video_path = os.path.join(VIDEOS_DIR, video_name)
        result = predict_video(video_path)
        result["video"] = video_name
        current_status = result
        print(f"[{current_index+1}/{len(videos)}] {video_name} → {result['label']} ({result['confidence']}%)")
        current_index = (current_index + 1) % len(videos)
        time.sleep(2)

thread = threading.Thread(target=analyze_next, daemon=True)
thread.start()

# ── Auth endpoints ────────────────────────────────────────────
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?',
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()

    if user:
        token = create_access_token(identity=username)
        return jsonify({"token": token, "username": username})
    return jsonify({"error": "Invalid credentials"}), 401

# ── Main endpoints ────────────────────────────────────────────
@app.route("/")
def index():
    return jsonify({"status": "Surveillance API running"})

@app.route("/status")
@jwt_required()
def status():
    return jsonify(current_status)

@app.route("/video/<filename>")
def serve_video(filename):
    return send_file(os.path.join(VIDEOS_DIR, filename))

if __name__ == "__main__":
    app.run(debug=False, port=5000)