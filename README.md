# Wildfire Detection Using YOLO on Jetson Nano

This project focuses on fine-tuning a YOLO object detection model to identify wildfires and smoke, and deploying it on an NVIDIA Jetson Nano.
https://github.com/user-attachments/assets/8201dfa7-0100-4763-8b89-b67dadb7bea9

## Project Structure
- `dataset/`: A privately annotated custom dataset used for training the wildfire detection model (Not included in this repository due to size constraints).
- `train/`: Contains scripts and configuration files for fine-tuning the YOLO model.
- `weights/`: Stores the trained model weights.
- `deploy/`: Includes scripts for deploying the model on the Jetson Nano:
  - `demo.py`: Main inference script running YOLO to detect "fire" and "smoke" in real-time.
  - `camera.py`: A utility script for capturing video streams and sending them for remote inference via socket.
  - `requirements_jetson.txt`: Specific dependencies and installation notes for Jetson Nano.
  - `best model.pt`: The fine-tuned YOLO model.
- `paper.docx`: Project documentation and related research.

## Requirements

### Standard Local Setup
To run standard training or inference on a regular machine (e.g., PC or Mac), install the dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Jetson Nano Setup & Deployment Guide
Deploying a custom YOLO model natively on a Jetson Nano requires specific environmental configurations to ensure hardware acceleration is utilized.

1. **Python Environment Setup**: 
   - The Jetson Nano (JetPack 4.6 / Ubuntu 18.04) defaults to Python 3.6.9, but Ultralytics YOLO requires Python 3.7+.
   - **Recommendation**: Create a virtual environment using Python 3.7+ (e.g., `virtualenv -p python3.7 venv`) rather than forcefully upgrading the global system Python. Upgrading the global Python breaks Jetson's local terminal dependencies.

2. **Installing Dependencies (Preserving CUDA Acceleration)**:
   - **Crucial Warning**: Do **NOT** run `pip install torch torchvision opencv-python` directly from PyPI. This installs CPU-only versions, ruining Jetson's native GPU performance.
   - You must manually install NVIDIA-optimized `.whl` files for PyTorch and Torchvision specifically built for JetPack.
   - For OpenCV, use the version that comes compiled with JetPack (which includes GStreamer support).

3. **Loading the Fine-Tuned Model**:
   - For real-time inference, ensure your code explicitly hands off processing to the GPU using `model.to('cuda')` (already implemented in `deploy/demo.py`). 

## Usage

1. **Model Inference**
   Run the deployment script to perform object detection using a connected camera.
   ```bash
   python deploy/demo.py
   ```

2. **Remote Camera Streaming**
   If you need to separate camera capture and inference due to hardware limitations (e.g., streaming from a Mac to Jetson Nano), run the sender script on the computer with the camera:
   ```bash
   python deploy/camera.py
   ```

## Deployment Challenges
For a detailed analysis of the deployment process, the challenges faced regarding Python versions and camera drivers on the Jetson Nano, and the workarounds implemented, please refer to the `Deployment_Process_and_Issue_Analysis.md` document.
