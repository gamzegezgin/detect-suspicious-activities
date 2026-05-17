import cv2
import numpy as np
from load_model import build_and_load

CLASSES    = ["Fighting", "Vandalism", "NormalVideos"]
SEQ_LEN    = 30
IMG_HEIGHT = 64
IMG_WIDTH  = 64

print("Model yükleniyor...")
model = build_and_load()
print("Model hazır.")

def predict_video(video_path):
    cap   = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total < SEQ_LEN:
        cap.release()
        return {"error": "Video too short"}

    indices = np.linspace(0, total - 1, SEQ_LEN, dtype=int)
    frames  = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
            frame = frame / 255.0
            frames.append(frame)

    cap.release()

    if len(frames) != SEQ_LEN:
        return {"error": "Could not read enough frames"}

    sequence   = np.array([frames])
    prediction = model.predict(sequence, verbose=0)
    class_idx  = int(np.argmax(prediction))
    confidence = float(prediction[0][class_idx])
    label      = CLASSES[class_idx]

    return {
        "label":      label,
        "confidence": round(confidence * 100, 2),
        "suspicious": label != "NormalVideos"
    }
