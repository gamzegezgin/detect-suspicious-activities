from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import threading
import time

sys.path.append(os.path.dirname(__file__))
from predict import predict_video

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Video klasörü — frontend/videos/ klasörü
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

# Arka planda analiz başlat
thread = threading.Thread(target=analyze_next, daemon=True)
thread.start()

@app.route("/")
def index():
    return jsonify({"status": "Surveillance API running"})

@app.route("/status")
def status():
    return jsonify(current_status)

@app.route("/video/<filename>")
def serve_video(filename):
    return send_file(os.path.join(VIDEOS_DIR, filename))

if __name__ == "__main__":
    app.run(debug=False, port=5000)