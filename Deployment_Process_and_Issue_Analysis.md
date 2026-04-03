# Process and Issue Analysis of Deploying Fine-tuned YOLO on Jetson Nano

During the deployment process, the core obstacle I initially encountered was Python version incompatibility. The official Jetson Nano OS is based on Ubuntu 18.04 and comes pre-installed with Python 3.6.9. However, Ultralytics YOLO requires Python 3.7 at a minimum, meaning I could not directly run `pip install`.

I then attempted to directly upgrade the system's Python version to 3.7. Although the upgrade was successful, the localized Jetson terminal relies on Python 3.6, causing the local terminal to fail to launch. To restore system functionality, I had to connect via SSH and downgrade Python back to its original version.

To avoid breaking the system environment, I switched to using a virtual environment to install Python 3.7. While this allowed YOLO to run normally, it rendered Jetson's built-in deep learning hardware acceleration packages (such as the CUDA-optimized Torch and Jetson-specific OpenCV) unusable. As an alternative, I had to install the standard public packages, but these packages could not utilize the Jetson's GPU acceleration, leading to a significant drop in operational performance.

Under these circumstances, I successfully managed to get CPU-based YOLO inference working first using standard OpenCV and Torch. But when I attempted to integrate a CSI camera, another issue emerged: standard OpenCV does not support GStreamer encoding on Jetson, making it impossible to directly read the camera feed.

To bypass this limitation, I designed a frontend-backend separation solution: the frontend used the system's Python 3.6 to read the camera's video stream and sent it via a Socket to the backend Python 3.7 environment running the YOLO model. Although the program structure was viable, the camera still failed to open. Further investigation revealed that the `/dev/video0` device existed, but the underlying i2c initialization failed. This indicated that the problem was likely due to physical damage to the camera hardware (about 80% probability) or a mismatch between the driver and the camera model (about 20% probability). Since Jetson drivers are closed-source, it was not possible to fix this independently.

As a temporary workaround, I used my Mac's camera to stream video over the local area network to the Jetson Nano for inference. This workflow ran smoothly, but due to the standard Torch lacking CUDA support, the inference speed was slow.

Later, I discovered that the official recommendation is to deploy using Docker. However, the image size is as large as 15GB, and downloading and building it on a Jetson Nano environment takes an incredibly long time. I haven't tried this approach yet, so I am unsure if it will trigger new issues.

### Next Steps In The Plan
1. Test and replace the camera (prioritize testing a USB camera to improve compatibility).
2. Re-evaluate the Docker deployment strategy to gain GPU acceleration support.
