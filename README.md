# Suspicious and Abnormal Human Activity Detection in Surveillance Systems Using AI-Based Models

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

## 🛠️ Tech Stack
* **Language:** Python
* **Deep Learning:** TensorFlow / Keras
* **Computer Vision:** OpenCV
* **Web Framework:** Flask
* **Data Handling:** NumPy, Pandas

## 👥 Project Team
This graduation thesis is a collaborative effort developed by:

| Team Member | Role | GitHub Profile |
|---|---|---|
| **Gamze Gezgin** | Researcher & Developer | [@gamzegezgin](https://github.com/gamzegezgin) |
| **Seryal Tuncer** | Researcher & Developer | [@Seryaltuncer](https://github.com/Seryaltuncer) |
| **Beyza K.** | Researcher & Developer | [@DevBeyzaK](https://github.com/DevBeyzaK) |

---
### 🎓 Supervisor
**Assoc. Prof. Dr. Faruk BULUT**
* GitHub: [@bulutfaruk](https://github.com/bulutfaruk)
* Istanbul Aydin University
* Software Engineering Department

---
