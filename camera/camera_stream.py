import cv2
import depthai as dai
from flask import Flask, Response
import threading
import time

app = Flask(__name__)

# Global Frame Storage
latest_frame = None


def camera_thread():
    global latest_frame

    print("[INFO] Starte DepthAI-Pipeline...")
    pipeline = dai.Pipeline()

    cam = pipeline.createColorCamera()
    cam.setPreviewSize(640, 480)
    cam.setInterleaved(False)
    cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

    xout = pipeline.createXLinkOut()
    xout.setStreamName("rgb")
    cam.preview.link(xout.input)

    with dai.Device(pipeline) as device:
        print("[INFO] DepthAI läuft.")
        q = device.getOutputQueue("rgb", maxSize=4, blocking=False)

        while True:
            in_rgb = q.tryGet()
            if in_rgb is None:
                time.sleep(0.01)
                continue

            latest_frame = in_rgb.getCvFrame()


def generate_frames():
    global latest_frame

    while True:
        if latest_frame is None:
            time.sleep(0.01)
            continue

        ret, buffer = cv2.imencode('.jpg', latest_frame)
        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def video_feed():
    print("[INFO] Browser verbunden.")
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # Kamera in separatem Thread starten
    t = threading.Thread(target=camera_thread, daemon=True)
    t.start()

    print("[INFO] Starte Webserver...")
    app.run(host='0.0.0.0', port=8080, threaded=True)
