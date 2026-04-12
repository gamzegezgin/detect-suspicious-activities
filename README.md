Suspicious and Abnormal Human Activity Detection in Surveillance Systems Using AI-Based Models
📌 Project Overview
This repository contains the source code and research materials for our undergraduate graduation thesis. The primary goal is to develop an automated system capable of detecting suspicious and abnormal human activities (fighting, vandalism, normal activities) in surveillance footage using a hybrid Deep Learning architecture combining VGG-16 for spatial feature extraction and LSTM for temporal sequence analysis.
🏗️ Architecture

Spatial Feature Extraction: Pre-trained VGG-16 CNN
Temporal Analysis: LSTM network for time-dependent pattern classification
Human Localization: YOLOv8 integration
Real-time API: Flask-based Web API with /predict endpoint
Database: MongoDB for storing predictions
Alerts: Twilio SMS notification module
Dashboard: Web-based real-time monitoring interface

📂 Datasets
The model is trained on a combined dataset built from the following sources:
Baseline

CAVIAR Dataset — Indoor surveillance footage used as the initial baseline for model evaluation.

Extended Training Set

UCF-Crime Dataset — Large-scale real-world surveillance dataset containing anomalous and normal activities. Used across all three classes.
Real Life Violence Situations Dataset — Contains real street fight videos collected from various sources. Added to the Fighting class (+1000 videos).
DCSASS Dataset — Surveillance footage containing vandalism and destructive behavior. Added to the Vandalism class (+200 videos).
KTH Action Dataset — Contains controlled recordings of human actions in outdoor environments. Added to the NormalVideos class (+600 videos).

Final Class Distribution
ClassSourcesAdditional VideosFightingUCF-Crime + Real Life Violence+1000VandalismUCF-Crime + DCSASS+200NormalVideosUCF-Crime + KTH+600
🛠️ Tech Stack

Language: Python
Deep Learning: TensorFlow / Keras
Computer Vision: OpenCV, YOLOv8
Web Framework: Flask
Database: MongoDB
Notifications: Twilio SMS
Data Handling: NumPy, Pandas

👥 Project Team
Team MemberRoleGitHubGamze GezginResearcher & Developer@gamzegezginSeryal TuncerResearcher & Developer@SeryaltuncerBeyza KonduResearcher & Developer@DevBeyzaK
🎓 Supervisor
Assoc. Prof. Dr. Faruk BULUT

Istanbul Aydin University, Software Engineering Department
