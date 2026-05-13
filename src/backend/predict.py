import random

CLASSES = ["Fighting", "Vandalism", "NormalVideos"]

def predict_video(video_path):
    # Geçici sahte tahmin — model hazır olunca değiştirilecek
    label      = random.choice(CLASSES)
    confidence = round(random.uniform(60, 99), 2)
    return {
        "label":      label,
        "confidence": confidence,
        "suspicious": label != "NormalVideos"
    }