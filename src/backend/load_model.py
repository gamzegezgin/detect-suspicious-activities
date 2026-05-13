from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    TimeDistributed, Bidirectional, LSTM,
    Dense, Dropout, GlobalAveragePooling2D
)
from tensorflow.keras.applications import MobileNetV2
import os

IMG_HEIGHT  = 64
IMG_WIDTH   = 64
SEQ_LEN     = 30
NUM_CLASSES = 3

def build_and_load():
    mobilenet = MobileNetV2(
        include_top=False,
        weights='imagenet',
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
    )
    mobilenet.trainable = False
    model = Sequential([
        TimeDistributed(mobilenet, input_shape=(SEQ_LEN, IMG_HEIGHT, IMG_WIDTH, 3)),
        TimeDistributed(GlobalAveragePooling2D()),
        Bidirectional(LSTM(64, return_sequences=False)),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(NUM_CLASSES, activation='softmax')
    ])

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    WEIGHTS  = os.path.join(BASE_DIR, "model", "model_weights.weights.h5")
    model.load_weights(WEIGHTS)
    print("Model yüklendi!")
    return model