# Suspicious Activity Detection in Surveillance Videos using Deep Learning

![Project Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Keras%20%7C%20TensorFlow-orange)

## 📌 Project Overview
This repository contains the source code and research materials for my undergraduate graduation thesis. The primary goal of this project is to develop an automated system capable of detecting suspicious and abnormal human activities (e.g., fighting, running, sudden movements) in surveillance footage.

The proposed solution utilizes a hybrid Deep Learning architecture combining **VGG-16** for feature extraction and **LSTM** (Long Short-Term Memory) for temporal sequence analysis.

## 🏗️ Proposed Architecture
The system will be built upon a two-stage deep learning pipeline:
1.  **Spatial Feature Extraction:** Using the pre-trained **VGG-16** CNN model to extract visual features from video frames.
2.  **Temporal Analysis:** Feeding the extracted feature sequences into an **LSTM** network to learn time-dependent patterns and classify activities as "Normal" or "Abnormal".

Finally, a **Flask-based Web API** will be developed to simulate real-time detection and generate alerts.

## 📂 Datasets
The model will be trained and evaluated on the following benchmark datasets:
* **KTH Action Dataset**
* **CAVIAR Dataset**
* **UCF-Crime Dataset**

## 🗓️ Project Roadmap
This project follows a structured timeline from December 2025 to June 2026.

- [ ] **Phase 1: Literature & Planning (Dec 2025)**
    - [ ] Review 3D-CNN and LSTM literature.
    - [ ] Design VGG-16 + LSTM architecture.
    - [ ] Initialize Git repository.

- [ ] **Phase 2: Data Acquisition (Jan 2026)**
    - [ ] Download KTH, CAVIAR, and UCF-Crime datasets.
    - [ ] Organize raw data into Normal/Abnormal classes.
    - [ ] Analyze dataset properties (resolution, frame rates).

- [ ] **Phase 3: Preprocessing (Feb 2026)**
    - [ ] Develop `preprocess.py` for video segmentation.
    - [ ] Implement frame extraction and normalization (e.g., 224x224 px).
    - [ ] Apply data augmentation techniques.

- [ ] **Phase 4: Model Development (Mar 2026)**
    - [ ] Implement VGG-16 and LSTM layers using Keras/Python.
    - [ ] Train the model (`train.py`) and monitor loss functions.
    - [ ] Hyperparameter optimization.

- [ ] **Phase 5: Evaluation (Apr 2026)**
    - [ ] Perform Cross-dataset validation.
    - [ ] Generate Confusion Matrix and calculate Accuracy/F1 Scores.
    - [ ] Comparative analysis with state-of-the-art models.

- [ ] **Phase 6: Deployment & Integration (May 2026)**
    - [ ] Develop Flask API and Web Interface.
    - [ ] Implement Alarm/Warning mechanism.
    - [ ] Run simulations with test videos.

- [ ] **Phase 7: Final Delivery (Jun 2026)**
    - [ ] Code cleanup and refactoring.
    - [ ] Record demo video.
    - [ ] Final thesis defense.

## 🛠️ Tech Stack
* **Language:** Python
* **Deep Learning:** TensorFlow / Keras
* **Computer Vision:** OpenCV
* **Web Framework:** Flask
* **Data Handling:** NumPy, Pandas


---
