from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import os
import sys
import threading
import time
import sqlite3
import hashlib
import requests
import cv2

sys.path.append(os.path.dirname(__file__))
from predict import predict_video

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = 'surveillance-secret-key-2026'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

# ── Telegram ─────────────────────────────────────────────────
TELEGRAM_TOKEN    = "8910446850:AAFRI5T5srghwQ2ZKstEyHLWfyPAf_ZEuRw"
TELEGRAM_CHAT_IDS = ["7574376004", "8327708889"]

def send_telegram(label, confidence, video_name):
    msg = (
        f"Suspicious behavior detected\n"
        f"Type: {label}\n"
        f"Camera: CAM-01"
    )
    for chat_id in TELEGRAM_CHAT_IDS:
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": msg},
                timeout=5
            )
        except Exception as e:
            print(f"Telegram hatasi ({chat_id}): {e}")

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

def is_valid_video(path):
    cap = cv2.VideoCapture(path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total < 90:
        cap.release()
        return False
    # %10 ile %90 arası 5 noktayı kontrol et
    for pos in [0.1, 0.3, 0.5, 0.7, 0.9]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(total * pos))
        ret, frame = cap.read()
        if not ret or frame.mean() < 20:
            cap.release()
            return False
    cap.release()
    return True

def get_video_duration(path):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    duration = frame_count / fps
    return max(3, min(duration, 10))

def analyze_next():
    global current_index, current_status
    while True:
        video_name = videos[current_index]
        video_path = os.path.join(VIDEOS_DIR, video_name)
        current_index = (current_index + 1) % len(videos)

        if not is_valid_video(video_path):
            print(f"Gecersiz video atlandi: {video_name}")
            continue

        current_status["video"] = video_name

        result = predict_video(video_path)
        result["video"] = video_name
        current_status = result

        label = result.get('label', '')
        confidence = result.get('confidence', 0)
        print(f"[{current_index}/{len(videos)}] {video_name} → {label} (%{confidence})")

        if label in ["Fighting", "Vandalism"]:
            send_telegram(label, confidence, video_name)

        wait = get_video_duration(video_path)
        time.sleep(wait)

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

@app.route("/next_video")
@jwt_required()
def next_video():
    try:
        current_video = current_status.get("video", videos[0])
        idx = videos.index(current_video)
        next_idx = (idx + 1) % len(videos)
        return jsonify({"video": videos[next_idx]})
    except:
        return jsonify({"video": videos[0]})

@app.route("/video/<filename>")
def serve_video(filename):
    return send_file(os.path.join(VIDEOS_DIR, filename))

if __name__ == "__main__":
    app.run(debug=False, port=5000)