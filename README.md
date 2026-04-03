# Wildfire Detection Using YOLO on Jetson Nano

This project focuses on fine-tuning a YOLO object detection model to identify wildfires and smoke, and deploying it on an NVIDIA Jetson Nano.

## Project Structure
- `dataset/`: Contains the dataset used for training the wildfire detection model.
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

### Jetson Nano Setup
**IMPORTANT:** Please refer to the instructions in `deploy/requirements_jetson.txt`. Do **NOT** directly `pip install torch`, `torchvision`, or `opencv-python` via standard PyPI on the Jetson Nano. Doing so will install CPU-only versions and break CUDA acceleration. Make sure to use NVIDIA-provided `.whl` files for PyTorch and compile or use the system OpenCV natively supported by JetPack OS.

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
