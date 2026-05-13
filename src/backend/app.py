from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import random

sys.path.append(os.path.dirname(__file__))
from predict import predict_video

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Sahte durum — model hazır olunca gerçekle değiştirilecek
current_status = {
    "label": "NormalVideos",
    "confidence": 91.0,
    "suspicious": False
}

@app.route("/")
def index():
    return jsonify({"status": "Surveillance API running"})

@app.route("/status")
def status():
    return jsonify(current_status)

@app.route("/predict", methods=["POST"])
def predict():
    if "video" not in request.files:
        return jsonify({"error": "No video file"}), 400

    file = request.files["video"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(video_path)

    result = predict_video(video_path)
    os.remove(video_path)

    global current_status
    current_status = result

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)