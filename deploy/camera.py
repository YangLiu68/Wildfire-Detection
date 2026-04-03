#!/usr/bin/env python3
import cv2
import socket
import struct
import time

JETSON_IP   = "192.168.102.170"
JETSON_PORT = 9999
CAM_INDEX   = 1                 
WIDTH, HEIGHT = 1280, 720
FPS = 30
JPEG_QUALITY = 80               # 70~90：越高越清晰，带宽越大

def main():
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        raise RuntimeError("Error: Could not open camera.")

    # 可选：设置分辨率/帧率（部分设备可能无效）
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS,          FPS)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((JETSON_IP, JETSON_PORT))
    print(f"[Sender] Connected to {JETSON_IP}:{JETSON_PORT}")

    enc_param = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
    n, t0 = 0, time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # 编码成 JPEG，便于网络传输
            ok, enc = cv2.imencode(".jpg", frame, enc_param)
            if not ok:
                continue
            data = enc.tobytes()

            # 发送：4 字节长度（网络字节序）+ 数据
            s.sendall(struct.pack("!I", len(data)))
            s.sendall(data)

            # 简单统计
            n += 1
            if n % 30 == 0:
                now = time.time()
                fps = 30 / (now - t0)
                t0 = now
                print(f"[Sender] ~{fps:.1f} FPS, pkt={len(data)/1024:.0f} KB")
    except KeyboardInterrupt:
        pass
    finally:
        s.close()
        cap.release()
        print("[Sender] Stopped.")

if __name__ == "__main__":
    main()
