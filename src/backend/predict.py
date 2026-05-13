import cv2
import numpy as np
import os
from ultralytics import YOLO
from load_model import build_and_load

CLASSES         = ["Fighting", "Vandalism", "NormalVideos"]
SEQ_LEN         = 30
IMG_HEIGHT      = 64
IMG_WIDTH       = 64
YOLO_CONF       = 0.15
PERSON_CLASS_ID = 0

print("Modeller yükleniyor...")
yolo_model = YOLO("yolov8n.pt")
model      = build_and_load()
print("Modeller hazır.")

def extract_roi_with_yolo(frame_bgr):
    results = yolo_model(frame_bgr, conf=YOLO_CONF,
                         classes=[PERSON_CLASS_ID], verbose=False)
    boxes = results[0].boxes

    if boxes is None or len(boxes) == 0:
        return np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), dtype=np.float32)

    xyxy = boxes.xyxy.cpu().numpy()
    h, w = frame_bgr.shape[:2]

    x1 = max(0, int(np.min(xyxy[:, 0])))
    y1 = max(0, int(np.min(xyxy[:, 1])))
    x2 = min(w, int(np.max(xyxy[:, 2])))
    y2 = min(h, int(np.max(xyxy[:, 3])))

    pad = 20
    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(w, x2 + pad)
    y2 = min(h, y2 + pad)

    if x2 <= x1 or y2 <= y1:
        return np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), dtype=np.float32)

    roi = frame_bgr[y1:y2, x1:x2]
    roi = cv2.resize(roi, (IMG_WIDTH, IMG_HEIGHT))
    return roi / 255.0

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
            roi = extract_roi_with_yolo(frame)
            frames.append(roi)
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