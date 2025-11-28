# ------------------------------------------------------------
# PIb Hand + Arm Steuerung (Optimierte Version)
# Ellbogen: 3D/2D Hybrid, stabilisiert
# Unterarmrotation: Handflächen-Normalen
# Finger: Original
# Schultern: auskommentiert / nicht aktiv
# ------------------------------------------------------------

import cv2
import math
import numpy as np
import depthai as dai
import mediapipe as mp
import time

import piblib.movements as robot
robot.startup()

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=1,
    refine_face_landmarks=False,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

THUMB_GAIN = 2
FINGER_GAIN = 5
ELBOW_GAIN = 1.3
FOREARM_GAIN = 9000

INVERT_FINGERS = False
INVERT_ELBOW_LEFT = True
INVERT_ELBOW_RIGHT = True
INVERT_FOREARM_LEFT = True
INVERT_FOREARM_RIGHT = False

# ------------------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------------------

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def smooth(prev, new, alpha=0.2):
    return prev*(1-alpha) + new*alpha

def angle_between_vectors(v1, v2):
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 < 1e-8 or n2 < 1e-8:
        return 0
    c = np.dot(v1/n1, v2/n2)
    return math.acos(np.clip(c, -1.0, 1.0))

def angle_between_points(a, b, c):
    v1 = a - b
    v2 = c - b
    ang = angle_between_vectors(v1, v2)
    return float((math.pi - ang) / math.pi)

def curl_to_amount(curl, invert=False):
    if invert:
        curl = 1 - curl
    return int(clamp(curl * 18000 - 9000, -9000, 9000))

# ------------------------------------------------------------
# Unterarmrotation über Handflächen-Normalen
# ------------------------------------------------------------

def compute_forearm_rotation(hand_lm):
    lm = hand_lm.landmark

    p0 = np.array([lm[0].x, lm[0].y, lm[0].z])
    p5 = np.array([lm[5].x, lm[5].y, lm[5].z])
    p17 = np.array([lm[17].x, lm[17].y, lm[17].z])

    v1 = p5 - p0
    v2 = p17 - p0
    normal = np.cross(v1, v2)

    if np.linalg.norm(normal) < 1e-6:
        return 0

    cam_z = np.array([0, 0, -1])

    ang = angle_between_vectors(normal, cam_z)
    val = (ang / math.pi) * 18000 - 9000
    return int(clamp(val, -9000, 9000))

# ------------------------------------------------------------
# Ellbogen: 3D + 2D fallback
# ------------------------------------------------------------

def compute_elbow_3d_angle(shoulder, elbow, wrist):
    v1 = shoulder - elbow
    v2 = wrist - elbow
    if np.linalg.norm(v1) < 1e-6 or np.linalg.norm(v2) < 1e-6:
        return None
    ang = angle_between_vectors(v1, v2)
    return float((math.pi - ang) / math.pi)

def compute_elbow_2d_angle_px(shoulder, elbow, wrist):
    v1 = np.array([shoulder[0]-elbow[0], shoulder[1]-elbow[1]])
    v2 = np.array([wrist[0]-elbow[0], wrist[1]-elbow[1]])
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 < 1e-6 or n2 < 1e-6:
        return None
    # normalisierte 2D Richtung
    v1n = v1 / n1
    v2n = v2 / n2
    c = np.clip(np.dot(v1n, v2n), -1.0, 1.0)
    ang = math.acos(c)
    return float((math.pi - ang) / math.pi)

def median(lst):
    if not lst:
        return 0
    a = sorted(lst)
    return a[len(a)//2]

# ------------------------------------------------------------
# Fingerprocessing
# ------------------------------------------------------------

def process_hand(hand_landmarks, side, state):
    if not hand_landmarks:
        return

    lm = hand_landmarks.landmark

    # Kleine Hilfsfunktion für Landmark → numpy Array
    def arr(i):
        p = lm[i]
        return np.array([p.x, p.y, p.z], dtype=float)

    # ---------------------------------------------------------
    # THUMB CURL – verbesserte Version
    # ---------------------------------------------------------

    # Finger- und Palmpunkte
    t2 = arr(2)
    t3 = arr(3)
    t4 = arr(4)
    p0 = arr(0)    # Handwurzel
    p5 = arr(5)    # Index-MCP
    p17 = arr(17)  # Pinky-MCP

    # (1) Originaler Winkel 2–3–4 (MediaPipe IP joint)
    curl_ip = angle_between_points(t2, t3, t4)

    # (2) Annäherung des Daumen zur Handfläche (gut frontal)
    dist_thumb_to_index = np.linalg.norm(t4 - p5)
    dist_norm = clamp(1.0 - dist_thumb_to_index * 2.2, 0.0, 1.0)

    # (3) Daumen-Richtung vs. Handflächen-Normale
    palm_normal = np.cross(p5 - p0, p17 - p0)
    thumb_dir = t4 - t2
    if np.linalg.norm(palm_normal) < 1e-8 or np.linalg.norm(thumb_dir) < 1e-8:
        curl_plane = 0.0
    else:
        palm_normal /= np.linalg.norm(palm_normal)
        thumb_dir   /= np.linalg.norm(thumb_dir)
        cosval = np.dot(palm_normal, thumb_dir)
        curl_plane = clamp((1 - cosval) * 0.5, 0.0, 1.0)

    # Mix aller 3 Signale
    thumb_curl = (curl_ip * 0.8) + (dist_norm * 0.15) + (curl_plane * 0.05)
    thumb_curl = clamp(thumb_curl, 0.0, 1.0)

    # Andere Finger
    curls = {
        "thumb":  thumb_curl,
        "index":  angle_between_points(arr(5), arr(6), arr(8)),
        "middle": angle_between_points(arr(9), arr(10), arr(12)),
        "ring":   angle_between_points(arr(13), arr(14), arr(16)),
        "pinky":  angle_between_points(arr(17), arr(18), arr(20)),
    }

    # In Servos überführen
    for k, c in curls.items():
        c = min(1.0, c * (THUMB_GAIN if k == "thumb" else FINGER_GAIN))
        amt = curl_to_amount(c, invert=INVERT_FINGERS)
        if k == "thumb":
            state[side][k] = amt  # KEIN smoothing für den Daumen
        else:
            state[side][k] = smooth(state[side][k], amt)

    # An Robot senden
    try:
        if side == "left":
            robot.turnLeftThumb(int(state[side]["thumb"]))
            robot.curlLeftThumb(int(state[side]["thumb"]))
            robot.curlLeftIndex(int(state[side]["index"]))
            robot.curlLeftMiddle(int(state[side]["middle"]))
            robot.curlLeftRing(int(state[side]["ring"]))
            robot.curlLeftPinky(int(state[side]["pinky"]))
        else:
            robot.turnRightThumb(int(state[side]["thumb"]))
            robot.curlRightThumb(int(state[side]["thumb"]))
            robot.curlRightIndex(int(state[side]["index"]))
            robot.curlRightMiddle(int(state[side]["middle"]))
            robot.curlRightRing(int(state[side]["ring"]))
            robot.curlRightPinky(int(state[side]["pinky"]))
        # print("thumb_curl:", thumb_curl)
        # print("amt:", amt)
        # print("FINAL:", state[side]["thumb"])
    except Exception as e:
        print("Robot finger send error:", e)


# ------------------------------------------------------------
# DepthAI Setup
# ------------------------------------------------------------

pipeline = dai.Pipeline()
cam = pipeline.createColorCamera()
cam.setPreviewSize(640, 480)
cam.setInterleaved(False)
cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

xout = pipeline.createXLinkOut()
xout.setStreamName("rgb")
cam.preview.link(xout.input)

# ------------------------------------------------------------
# State
# ------------------------------------------------------------

state = {
    "left":  {"thumb":0,"index":0,"middle":0,"ring":0,"pinky":0,
              "elbow":0,"forearm":0, "elbow_hist":[], "elbow_prev":0,
              "shoulderL": 0, "shoulder_prev_L": None},
    "right": {"thumb":0,"index":0,"middle":0,"ring":0,"pinky":0,
              "elbow":0,"forearm":0, "elbow_hist":[], "elbow_prev":0,
              "shoulderR": 0, "shoulder_prev_R": None},
}



ELBOW_HIST_LEN = 5
ELBOW_MAX_DELTA = 1500

# ------------------------------------------------------------
# Main Loop
# ------------------------------------------------------------

with dai.Device(pipeline) as device:
    q_rgb = device.getOutputQueue("rgb", maxSize=4, blocking=False)

    while True:
        frame = q_rgb.get().getCvFrame()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = holistic.process(rgb)
        debug = frame.copy()

        # Hände
        process_hand(results.left_hand_landmarks, "left", state)
        process_hand(results.right_hand_landmarks, "right", state)

        # Zeichnen Hände
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(debug, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(debug, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # -------------------------------------------------------
        # ELLBOGEN + FOREARM
        # -------------------------------------------------------
        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            # print("POSE FOUND")
            # print("Left shoulder Y:", lm[11].y, "Left hip Y:", lm[23].y)
            # print("Right shoulder Y:", lm[12].y, "Right hip Y:", lm[24].y)


            # Punkte als Arrays
            Ls = np.array([lm[11].x, lm[11].y, lm[11].z])
            Le = np.array([lm[13].x, lm[13].y, lm[13].z])
            Lw = np.array([lm[15].x, lm[15].y, lm[15].z])

            Rs = np.array([lm[12].x, lm[12].y, lm[12].z])
            Re = np.array([lm[14].x, lm[14].y, lm[14].z])
            Rw = np.array([lm[16].x, lm[16].y, lm[16].z])

            # Ellbogen-Winkel 3D/2D
            el3d_L = compute_elbow_3d_angle(Ls, Le, Lw)
            el3d_R = compute_elbow_3d_angle(Rs, Re, Rw)

            el2d_L = compute_elbow_2d_angle_px(Ls, Le, Lw)
            el2d_R = compute_elbow_2d_angle_px(Rs, Re, Rw)

            # Mischung
            def mix(a, b):
                if a is None and b is None: return 0
                if a is None: return b
                if b is None: return a
                return 0.7*a + 0.3*b  # 3D bevorzugt

            blend_L = mix(el3d_L, el2d_L)
            blend_R = mix(el3d_R, el2d_R)

            blend_L = clamp(blend_L * ELBOW_GAIN, 0, 1)
            blend_R = clamp(blend_R * ELBOW_GAIN, 0, 1)

            amt_L = curl_to_amount(blend_L, invert=INVERT_ELBOW_LEFT)
            amt_R = curl_to_amount(blend_R, invert=INVERT_ELBOW_RIGHT)

            # Median-Filter
            def apply_hist(side, val):
                h = state[side]["elbow_hist"]
                h.append(val)
                if len(h) > ELBOW_HIST_LEN:
                    h.pop(0)
                return median(h)

            med_L = apply_hist("left", amt_L)
            med_R = apply_hist("right", amt_R)

            # Smooth velocity clamp
            def vel(side, val):
                prev = state[side]["elbow_prev"]
                delta = val - prev
                if abs(delta) > ELBOW_MAX_DELTA:
                    val = prev + np.sign(delta) * ELBOW_MAX_DELTA
                out = int(smooth(prev, val, 0.25))
                state[side]["elbow_prev"] = out
                return out

            state["left"]["elbow"] = vel("left", med_L)
            state["right"]["elbow"] = vel("right", med_R)

            # Forearm
            if results.left_hand_landmarks:
                fL = compute_forearm_rotation(results.left_hand_landmarks)
                if INVERT_FOREARM_LEFT: fL = -fL
                state["left"]["forearm"] = smooth(state["left"]["forearm"], fL)

            if results.right_hand_landmarks:
                fR = compute_forearm_rotation(results.right_hand_landmarks)
                if INVERT_FOREARM_RIGHT: fR = -fR
                state["right"]["forearm"] = smooth(state["right"]["forearm"], fR)

            # Send to robot
            robot.curlLeftEllbow(int(state["left"]["elbow"]))
            robot.curlRightEllbow(int(state["right"]["elbow"]))
            robot.turnLeftUnderarm(int(state["left"]["forearm"]))
            robot.turnRightUnderarm(int(state["right"]["forearm"]))

            # -------------------------------------------------------
            # SHOULDERS – Arm nach vorne heben (Flexion)
            # -------------------------------------------------------

            # Hüfte-Punkte
          # Lh = np.array([lm[23].x, lm[23].y, lm[23].z])
          # Rh = np.array([lm[24].x, lm[24].y, lm[24].z])

          # # Vektoren Schulter → Ellbogen
          # uL = Le - Ls
          # uR = Re - Rs

          # # Vektoren Schulter → Hüfte (Referenz nach unten)
          # refL = Lh - Ls
          # refR = Rh - Rs


          # def compute_shoulder_flexion(u, ref):
          #     if np.linalg.norm(u) < 1e-6 or np.linalg.norm(ref) < 1e-6:
          #         return 0

          #     # Normieren
          #     u_n = u / np.linalg.norm(u)
          #     ref_n = ref / np.linalg.norm(ref)

          #     # Winkel zwischen beiden (0..π)
          #     angle = angle_between_vectors(u_n, ref_n)

          #     # Mapping:
          #     # Arm unten -> angle = 0 → 0.0
          #     # Arm vorne oben 90° → angle = ~1.57 → 1.0
          #     norm = clamp(angle / (math.pi / 2), 0.0, 1.0)

          #     return norm


          # # Werte 0..1
          # L_val = compute_shoulder_flexion(uL, refL)
          # R_val = compute_shoulder_flexion(uR, refR)

          # # Servo mappen (-9000..+9000)
          # L_amt = int((L_val * 2.0 - 1.0) * 9000)
          # R_amt = int((R_val * 2.0 - 1.0) * 9000)

          # # Glätten
          # state["left"]["shoulderL"] = smooth(state["left"]["shoulderL"], L_amt, 0.25)
          # state["right"]["shoulderR"] = smooth(state["right"]["shoulderR"], R_amt, 0.25)

          # # An Robot senden
          # robot.turnLeftShoulderVert(int(state["left"]["shoulderL"]))
          # robot.turnRightShoulderVert(int(state["right"]["shoulderR"]))

          # mp_drawing.draw_landmarks(debug, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        # -------------------------------------------------------
        cv2.imshow("PIb Optimized", debug)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
