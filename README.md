# 🌿 DeepStream 7.0 Weed Detection Pipeline with YOLOv9 + PostgreSQL + Grafana

This repository implements an end-to-end object detection pipeline using **YOLOv9** and **DeepStream 7.0** for weed detection in agricultural fields. The predictions are stored in a **PostgreSQL** database and connected to **Grafana** for real-time data visualization and analysis.

<p align="center">
  <img src="https://github.com/TejasARathod/AgriDoc-WeedDetection-Deepstream/blob/13ffdafe6cdc202d9b23ffd8236fd0a07e5b4baf/Architecture.png?raw=true" width="700" />
</p>

---

## 📚 Table of Contents

* [🔍 Motivation](#-motivation)
* [📦 Environment Setup](#-environment-setup)
* [📁 Dataset](#-dataset)
* [🧠 Model Training](#-model-training)
* [📦 YOLOv9 to ONNX Export](#-yolov9-to-onnx-export)
* [🚀 DeepStream Deployment](#-deepstream-deployment)
* [💃 Kafka & PostgreSQL Integration](#-kafka--postgresql-integration)
* [📊 Grafana Visualization](#-grafana-visualization)
* [🎥 Demo Video](#-demo-video)
* [📄 Citations](#-citations)

---

## 🔍 Motivation

Precision weed detection in agriculture helps optimize herbicide usage and protect crops. This project brings together cutting-edge tools like YOLOv9, DeepStream, PostgreSQL, and Grafana to build a robust, real-time detection and analysis system deployable on the edge.

---

## 📦 Environment Setup

### 📃 Docker Container for DeepStream

We use NVIDIA’s DeepStream container for deployment:

```bash
docker pull nvcr.io/nvidia/deepstream:7.0-gc-triton-devel
```

### 🐍 Python Environment (for training, Kafka, PostgreSQL)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📁 Dataset

**Title:** Dataset of Annotated Food Crops and Weed Images for Robotic Computer Vision Control
**Authors:** Kaspars Sudars, Janis Jasko, Ivars Namatevs, Liva Ozola, Niks Badaukis
**Journal:** *Data in Brief*, Volume 31, 2020
**DOI:** [10.1016/j.dib.2020.105833](https://doi.org/10.1016/j.dib.2020.105833)
**Link:** [ScienceDirect Article](https://www.sciencedirect.com/science/article/pii/S2352340920307277)

---

## 🧠 Model Training

We trained YOLOv9 using the official [YOLOv9 repository](https://github.com/WongKinYiu/yolov9).

### 🛠️ Training Command:

```bash
python3 train_dual.py \
  --workers 4 \
  --device 0 \
  --batch 1 \
  --data data.yaml \
  --img 1280 \
  --cfg models/detect/yolov9-s.yaml \
  --weights '' \
  --name yolov9-c \
  --hyp hyp.scratch-high.yaml \
  --min-items 0 \
  --epochs 50 \
  --close-mosaic 10
```

> ⚠️ **Note:** GTX series GPUs face AMP-related issues, so `train_dual.py` was modified to disable AMP support.

---

## 📦 YOLOv9 to ONNX Export

Export the trained YOLOv9 model to ONNX using this [guide](https://github.com/marcoslucianops/DeepStream-Yolo/blob/master/docs/YOLOv9.md).

---

## 🚀 DeepStream Deployment

We used [DeepStream-Yolo](https://github.com/marcoslucianops/DeepStream-Yolo.git) to integrate YOLOv9 with DeepStream 7.0.

**Configured Files:**

* `deepstream_app_config.txt`
* `msg_conv.txt`
* `labels.txt`
* `config_infer_primary_yoloV9.txt`

Set CUDA version:

```bash
export CUDA_VER=12.2
```

Reference Documentation: [DeepStream Reference App](https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_ref_app_deepstream.html)

---

## 💃 Kafka & PostgreSQL Integration

### ▶️ Start Kafka Broker (in parallel):

```bash
sudo docker run -d -p 9092:9092 --name broker apache/kafka-native:latest
```

### ▶️ Run the Consumer:

1. Activate Python environment.
2. Install dependencies from `requirements.txt`.
3. Run `consumer.py`:

   * Creates a PostgreSQL table if not exists.
   * Stores inference results from Kafka.

PostgreSQL Docs: [Install on Ubuntu](https://www.postgresql.org/download/linux/ubuntu/)

---

## 📊 Grafana Visualization

Grafana connects to the PostgreSQL database for dashboard analytics.

<p align="center">
  <img src="https://github.com/TejasARathod/AgriDoc-WeedDetection-Deepstream/blob/13ffdafe6cdc202d9b23ffd8236fd0a07e5b4baf/Grafana-Dashboard.png?raw=true" width="700" />
</p>

Grafana Docs: [Install Grafana on Debian/Ubuntu](https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/)

---

## 🎥 Demo Video

<p align="center">
  <img src="https://github.com/TejasARathod/AgriDoc-WeedDetection-Deepstream/blob/13ffdafe6cdc202d9b23ffd8236fd0a07e5b4baf/Demo.gif?raw=true" width="600" />
</p>

**Demo Flow:**

1. Start Kafka Docker container
2. Start DeepStream pipeline
3. Start the Python `consumer.py` to log predictions into PostgreSQL
4. Play the RTSP video stream to trigger inference

---

## 📄 Citations

Please cite the following works if using this project:

```bibtex
@article{wang2024yolov9,
  title={{YOLOv9}: Learning What You Want to Learn Using Programmable Gradient Information},
  author={Wang, Chien-Yao and Liao, Hong-Yuan Mark},
  booktitle={arXiv preprint arXiv:2402.13616},
  year={2024}
}

@article{chang2023yolor,
  title={{YOLOR}-Based Multi-Task Learning},
  author={Chang, Hung-Shuo and Wang, Chien-Yao and Wang, Richard Robert and Chou, Gene and Liao, Hong-Yuan Mark},
  journal={arXiv preprint arXiv:2309.16921},
  year={2023}
}
```

---

## 🙌 Acknowledgments

* [YOLOv9 by WongKinYiu](https://github.com/WongKinYiu/yolov9)
* [DeepStream-Yolo by marcoslucianops](https://github.com/marcoslucianops/DeepStream-Yolo)

