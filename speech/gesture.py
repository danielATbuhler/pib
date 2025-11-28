# -*- coding: utf-8 -*-
"""
Vollständiges PiB-Gesten-Skript
Mit relativen Schulterbewegungen zu den Neutralwerten:

Linke Schulter Horizontal  -> Pin 0 = 8000
Linke Schulter Vertikal    -> Pin 1 = 9000
Rechte Schulter Horizontal -> Pin 8 = -8000
Rechte Schulter Vertikal   -> Pin 9 = -9000
"""

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_servo_v2 import BrickletServoV2
import time
import random

# ----------------------
# Konfiguration (UIDs)
# ----------------------
UID_RIGHT_HAND = "2b7m"    # bricklet_1
UID_SHOULDERS  = "2b7W"    # bricklet_2
UID_LEFT_HAND  = "2b83"    # bricklet_3

# ----------------------
# Verbindung
# ----------------------
ipcon = IPConnection()
servoRH = BrickletServoV2(UID_RIGHT_HAND, ipcon)
servoSH = BrickletServoV2(UID_SHOULDERS,  ipcon)
servoLH = BrickletServoV2(UID_LEFT_HAND,  ipcon)

ipcon.connect("localhost", 4223)

# ----------------------
# Limits
# ----------------------
POS_MIN = -9000
POS_MAX = 9000

# Schulter-Neutralwerte (von dir vorgegeben)
SH_L_HORZ_NEUTRAL =  8000
SH_L_VERT_NEUTRAL =  5000
SH_R_HORZ_NEUTRAL = -8000
SH_R_VERT_NEUTRAL = -5000

# Kopf-Limits
HEAD_TURN_SAFE = 3000
HEAD_TILT_SAFE = 700

# Finger-Limits
FINGER_RELAX = 0
FINGER_CURL  = 7000

def pause(t=0.06):
    time.sleep(t)

# ----------------------
# Hilfsfunktionen
# ----------------------
def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def safe_set_position(srv, pin, pos):
    pos = clamp(pos, POS_MIN, POS_MAX)
    srv.set_position(pin, int(pos))
    time.sleep(0.01)

# ----------------------
# Pulse widths
# ----------------------
def setup_pw(servo):
    for p in range(10):
        servo.set_pulse_width(p, 530, 2470)

setup_pw(servoRH)
setup_pw(servoLH)

servoSH.set_pulse_width(0, 530, 2470)
servoSH.set_pulse_width(1, 530, 2470)
servoSH.set_pulse_width(4, 530, 2470)
servoSH.set_pulse_width(5, 1250, 1850)
servoSH.set_pulse_width(8, 530, 2470)
servoSH.set_pulse_width(9, 530, 2470)

# Enable pins
def enable_slow(servo, pin):
    try:
        servo.set_enable(pin, True)
        time.sleep(0.15)   # Servos nicht gleichzeitig aktivieren!
    except:
        pass

for pin in range(10):
    enable_slow(servoRH, pin)
    enable_slow(servoLH, pin)
for pin in (0,1,4,5,8,9):
    enable_slow(servoSH, pin)

# ----------------------
# NEUTRALPOSITION
# ----------------------
NEUTRAL_POS = {
    # Hände
    **{(servoRH,p): 0 for p in range(10)},
    **{(servoLH,p): 0 for p in range(10)},

    # Schultern
    (servoSH,0): SH_L_HORZ_NEUTRAL,
    (servoSH,1): SH_L_VERT_NEUTRAL,
    (servoSH,4): 0,
    (servoSH,5): 0,
    (servoSH,8): SH_R_HORZ_NEUTRAL,
    (servoSH,9): SH_R_VERT_NEUTRAL
}

print("Fahre in Neutralposition...")
for (srv,pin),pos in NEUTRAL_POS.items():
    safe_set_position(srv, pin, pos)
pause(0.2)
print("Neutral erreicht.")

# ----------------------
# Relative Schulterbewegungen
# ----------------------
def right_shoulder(h, v, elbow=0, up=0, low=0):
    # Relativ zum Neutralwert
    safe_set_position(servoSH, 8, SH_R_HORZ_NEUTRAL + h)
    safe_set_position(servoSH, 9, SH_R_VERT_NEUTRAL + v)

    safe_set_position(servoRH, 8, elbow)
    safe_set_position(servoRH, 9, up)
    safe_set_position(servoRH, 7, low)

def left_shoulder(h, v, elbow=0, up=0, low=0):
    safe_set_position(servoSH, 0, SH_L_HORZ_NEUTRAL + h)
    safe_set_position(servoSH, 1, SH_L_VERT_NEUTRAL + v)

    safe_set_position(servoLH, 8, elbow)
    safe_set_position(servoLH, 9, up)
    safe_set_position(servoLH, 7, low)

# ----------------------
# Kopfsteuerung
# ----------------------
def head_turn_and_tilt(turn, tilt):
    safe_set_position(servoSH, 4, clamp(turn, -HEAD_TURN_SAFE, HEAD_TURN_SAFE))
    safe_set_position(servoSH, 5, clamp(tilt, -HEAD_TILT_SAFE, HEAD_TILT_SAFE))

# ----------------------
# Fingerfunktionen
# ----------------------
def move_all_fingers_right(pos):
    for p in range(6):
        safe_set_position(servoRH, p, pos)

def move_all_fingers_left(pos):
    for p in range(6):
        safe_set_position(servoLH, p, pos)

def relax_fingers_both():
    move_all_fingers_right(FINGER_RELAX)
    move_all_fingers_left(FINGER_RELAX)

# ---------------------------------------------------
#                 RECHTE GESTEN
# ---------------------------------------------------
def r_g1_small_wave():
    for _ in range(3):
        right_shoulder(1200,1200, elbow=1000); pause(0.18)
        right_shoulder(-1200,1000, elbow=500); pause(0.18)
    relax_fingers_both()

def r_g2_point():
    right_shoulder(1200,800, elbow=-1500)
    relax_fingers_both()
    safe_set_position(servoRH,2,-FINGER_CURL)
    pause(0.4)
    relax_fingers_both()

def r_g3_big_circle():
    for pos in [-1500,0,1500,3000,1500,0]:
        right_shoulder(pos,1000, elbow=pos//2); pause(0.2)
    relax_fingers_both()

def r_g4_double_tap_air():
    for _ in range(2):
        right_shoulder(800,900); pause(0.12)
        right_shoulder(1000,1100); pause(0.12)
    relax_fingers_both()

def r_g5_push_forward():
    for v in [900,600,900,600]:
        right_shoulder(0,v); pause(0.18)
    relax_fingers_both()

def r_g6_open_sweep():
    for h in [-1500,-2500,-3200,-2500,-1500]:
        right_shoulder(h,1000); pause(0.18)
    relax_fingers_both()

def r_g7_emphatic_rotation():
    for rot in [-1200,1200,-800]:
        safe_set_position(servoRH,7,rot); pause(0.18)
    relax_fingers_both()

def r_g8_halfcircle_forward():
    for h in [0,1200,2400,1200,0]:
        right_shoulder(h,1200); pause(0.18)
    relax_fingers_both()

def r_g9_wide_wave():
    for h in [-2000,2000,-2000,2000]:
        right_shoulder(h,1000); pause(0.18)
    relax_fingers_both()

def r_g10_elbow_flick():
    for e in [-1000,1000,-500]:
        safe_set_position(servoRH,8,e); pause(0.15)
    relax_fingers_both()

# ---------------------------------------------------
#                 LINKE GESTEN
# ---------------------------------------------------
def l_g1_small_wave():
    for _ in range(3):
        left_shoulder(-1200,1200, elbow=1000); pause(0.18)
        left_shoulder(1200,1000, elbow=500); pause(0.18)
    relax_fingers_both()

def l_g2_point():
    left_shoulder(-1200,800, elbow=-1500)
    relax_fingers_both()
    safe_set_position(servoLH,2,-FINGER_CURL)
    pause(0.4)
    relax_fingers_both()

def l_g3_big_circle():
    for pos in [1500,0,-1500,-3000,-1500,0]:
        left_shoulder(pos,1000, elbow=pos//2); pause(0.2)
    relax_fingers_both()

def l_g4_double_tap_air():
    for _ in range(2):
        left_shoulder(-800,900); pause(0.12)
        left_shoulder(-1000,1100); pause(0.12)
    relax_fingers_both()

def l_g5_push_left():
    for v in [900,600,900,600]:
        left_shoulder(0,v); pause(0.18)
    relax_fingers_both()

def l_g6_open_sweep():
    for h in [1500,2500,3200,2500,1500]:
        left_shoulder(h,1000); pause(0.18)
    relax_fingers_both()

def l_g7_emphatic_rotation():
    for rot in [1200,-1200,800]:
        safe_set_position(servoLH,7,rot); pause(0.18)
    relax_fingers_both()

def l_g8_halfcircle_forward():
    for h in [0,-1200,-2400,-1200,0]:
        left_shoulder(h,1200); pause(0.18)
    relax_fingers_both()

def l_g9_wide_wave():
    for h in [2000,-2000,2000,-2000]:
        left_shoulder(h,1000); pause(0.18)
    relax_fingers_both()

def l_g10_elbow_flick():
    for e in [1000,-1000,500]:
        safe_set_position(servoLH,8,e); pause(0.15)
    relax_fingers_both()

# ---------------------------------------------------
#                   KOPF-GESTEN
# ---------------------------------------------------
def head_nod():
    head_turn_and_tilt(0,300); pause(0.15)
    head_turn_and_tilt(0,-200); pause(0.15)
    head_turn_and_tilt(0,0)

def head_shake():
    head_turn_and_tilt(-1000,0); pause(0.15)
    head_turn_and_tilt(1000,0); pause(0.15)
    head_turn_and_tilt(0,0)

def head_look_up():
    head_turn_and_tilt(0,-HEAD_TILT_SAFE); pause(0.25)
    head_turn_and_tilt(0,0)

def head_look_side_and_tilt():
    head_turn_and_tilt(1200,200); pause(0.25)
    head_turn_and_tilt(-800,-150); pause(0.25)
    head_turn_and_tilt(0,0)

def head_thoughtful():
    head_turn_and_tilt(600,150); pause(0.3)
    head_turn_and_tilt(0,0)

HEAD_GESTURES = [
    head_nod, head_shake, head_look_up,
    head_look_side_and_tilt, head_thoughtful
]

# ---------------------------------------------------
#            Gesamtliste aller Gesten
# ---------------------------------------------------
ALL_GESTURES = [
    l_g1_small_wave, l_g2_point, l_g3_big_circle, l_g4_double_tap_air, l_g5_push_left,
    l_g6_open_sweep, l_g7_emphatic_rotation, l_g8_halfcircle_forward, l_g9_wide_wave, l_g10_elbow_flick,

    r_g1_small_wave, r_g2_point, r_g3_big_circle, r_g4_double_tap_air, r_g5_push_forward,
    r_g6_open_sweep, r_g7_emphatic_rotation, r_g8_halfcircle_forward, r_g9_wide_wave, r_g10_elbow_flick
]

# ---------------------------------------------------
#                Ablaufsteuerung
# ---------------------------------------------------
def make_gesture_async(done_event):
    try:
        choices = ALL_GESTURES + HEAD_GESTURES

        while not done_event.is_set():   # weitergesteikulieren solange gesprochen wird
            g = random.choice(choices)
            g()
            pause(0.3)

        # nach Sprechen: Neutral
        for (srv,pin),pos in NEUTRAL_POS.items():
            safe_set_position(srv,pin,pos)
            pause(0.02)

    except Exception as e:
        print("Gesture Error:", e)


# ---------------------------------------------------
# Shutdown
def shutdown():
    for p in range(10):
        try:
            servoRH.set_enable(p, False)
            servoLH.set_enable(p, False)
            if p in (0,1,4,5,8,9):
                servoSH.set_enable(p, False)
        except:
            pass

    ipcon.disconnect()
    print("Roboter deaktiviert.")
    return 0
