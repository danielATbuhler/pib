import time
import json

from mediapipe.util.analytics.mediapipe_logging_enums_pb2 import MODE_UNKNOWN
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_servo_v2 import BrickletServoV2

servoConfPath = "./piblib/servo_conf.json"
with open(servoConfPath, 'r') as servoConfFile:
    servoConf = json.load(servoConfFile)

UID_RIGHT_HAND = servoConf['bricklet_ids']['bricklet_1']
UID_ARM_HEAD = servoConf['bricklet_ids']['bricklet_2']
UID_LEFT_HAND = servoConf['bricklet_ids']['bricklet_3']

scRightHand = servoConf['servo_configurations']['right_hand']
scHeadShoulder = servoConf['servo_configurations']['head_shoulder']
scLeftHand = servoConf['servo_configurations']['left_hand']


UIDS = [UID_LEFT_HAND, UID_ARM_HEAD, UID_RIGHT_HAND]

ipcon = IPConnection()

slh = BrickletServoV2(UID_LEFT_HAND,ipcon)
sah = BrickletServoV2(UID_ARM_HEAD, ipcon)
srh = BrickletServoV2(UID_RIGHT_HAND, ipcon)

ipcon.connect('localhost', 4223)

POS_MIN = 9000
POS_MAX = -9000

#---------------------------------------
# Startup
#---------------------------------------
def stdSettings():
    # Left Hand
    pin=0
    for servo in scLeftHand:
        slh.set_pulse_width(pin,scLeftHand[servo]['pw_min'],scLeftHand[servo]['pw_max'])
        slh.set_motion_configuration(pin,scLeftHand[servo]['velocity'],scLeftHand[servo]['acceleration'],scLeftHand[servo]['deceleration'])
        pin+=1

    #Arm and Head
    pin=0
    for servo in scHeadShoulder:
        sah.set_pulse_width(pin,scHeadShoulder[servo]['pw_min'],scHeadShoulder[servo]['pw_max'])
        sah.set_motion_configuration(pin,scHeadShoulder[servo]['velocity'],scHeadShoulder[servo]['acceleration'],scHeadShoulder[servo]['deceleration'])
        if pin == 1 or pin == 5:
            pin += 3
        else:
            pin+=1

    # Right Hand
    pin=0
    for servo in scRightHand:
        srh.set_pulse_width(pin,scRightHand[servo]['pw_min'],scRightHand[servo]['pw_max'])
        srh.set_motion_configuration(pin,scRightHand[servo]['velocity'],scRightHand[servo]['acceleration'],scRightHand[servo]['deceleration'])
        pin+=1

def startup():
    stdSettings()
    time.sleep(1)
    relaxPos()

    for i in range(10):
        time.sleep(0.05)
        slh.set_enable(i,True)
        time.sleep(0.05)
        sah.set_enable(i,True)
        time.sleep(0.05)
        srh.set_enable(i,True)
    print('setup done')


def rhInvert(pin):
    for name, obj in scRightHand.items():
        if obj.get("pin") == pin:
            target = obj
            return(target['invert'])
    return False


def haInvert(pin):
    for name, obj in scHeadShoulder.items():
        if obj.get("pin") == pin:
            target = obj
            return(target['invert'])
    return False


def lhInvert(pin):
    for name, obj in scLeftHand.items():
        if obj.get("pin") == pin:
            target = obj
            return(target['invert'])
    return False

#---------------------------------------
# Base Movements
#---------------------------------------

# Left Hand
def turnLeftThumb(amount):
    pin = 0
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

def curlLeftThumb(amount):
    pin = 1
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

def curlLeftIndex(amount):
    pin = 2
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

def curlLeftMiddle(amount):
    pin = 3
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

def curlLeftRing(amount):
    pin = 4
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

def curlLeftPinky(amount):
    pin = 5
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

def curlLeftWrist(amount):
    pin = 6
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

#Right Hand
def turnRightThumb(amount):
    pin = 0
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin, amount)

def curlRightThumb(amount):
    pin = 1
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin, amount)

def curlRightIndex(amount):
    pin = 2
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin, amount)

def curlRightMiddle(amount):
    pin = 3
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin, amount)

def curlRightRing(amount):
    pin = 4
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin, amount)

def curlRightPinky(amount):
    pin = 5
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin, amount)

def curlRightWrist(amount):
    pin = 6
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin, amount)

#Arms
def turnLeftUnderarm(amount):
    pin = 7
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

def turnRightUnderarm(amount):
    pin = 7
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin7, amount)

def curlLeftEllbow(amount):
    pin = 8
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

def curlRightEllbow(amount):
    pin = 8
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin, amount)

def turnLeftUperarm(amount):
    pin = 9
    if lhInvert(pin):
        amount *= (-1)
    slh.set_position(pin, amount)

def turnRightUperarm(amount):
    pin = 9
    if rhInvert(pin):
        amount *= (-1)
    srh.set_position(pin, amount)


#Shoulders
def turnLeftShoulderHor(amount):
    pin = 0
    if haInvert(pin):
        amount *= (-1)
    sah.set_position(pin,amount)

def turnLeftShoulderVert(amount):
    pin = 1
    if haInvert(pin):
        amount *= (-1)
    sah.set_position(pin,amount)

def turnRightShoulderHor(amount):
    pin = 8
    if haInvert(pin):
        amount *= (-1)
    sah.set_position(pin,amount)

def turnRightShoulderVert(amount):
    pin = 9
    if haInvert(pin):
        amount *= (-1)
    sah.set_position(pin,amount)


#Head
def turnHeadHor(amount):
    pin = 4
    if haInvert(pin):
        amount *= (-1)
    sah.set_position(pin,amount)

def turnHeadVert(amount):
    pin = 5
    if haInvert(pin):
        amount *= (-1)
    sah.set_position(pin,amount)


#---------------------------------------
# Small part Movements
#---------------------------------------

#Left Fingers
def relaxLeftFingers():
    turnLeftThumb(POS_MAX)
    curlLeftThumb(POS_MAX)
    curlLeftIndex(POS_MAX)
    curlLeftMiddle(POS_MAX)
    curlLeftRing(POS_MAX)
    curlLeftPinky(POS_MAX)

def moveLeftFingers(amount):
    turnLeftThumb(amount)
    curlLeftThumb(amount)
    curlLeftIndex(amount)
    curlLeftMiddle(amount)
    curlLeftRing(amount)
    curlLeftPinky(amount)

def curlLeftFingers():
    turnLeftThumb(POS_MIN)
    curlLeftThumb(POS_MIN)
    curlLeftIndex(POS_MIN)
    curlLeftMiddle(POS_MIN)
    curlLeftRing(POS_MIN)
    curlLeftPinky(POS_MIN)

#Right Fingers
def relaxRightFingers():
    turnRightThumb(POS_MAX)
    curlRightThumb(POS_MAX)
    curlRightIndex(POS_MAX)
    curlRightMiddle(POS_MAX)
    curlRightRing(POS_MAX)
    curlRightPinky(POS_MAX)

def moveRightFingers(amount):
    turnRightThumb(amount)
    curlRightThumb(amount)
    curlRightIndex(amount)
    curlRightMiddle(amount)
    curlRightRing(amount)
    curlRightPinky(amount)

def curlRightFingers():
    turnRightThumb(POS_MIN)
    curlRightThumb(POS_MIN)
    curlRightIndex(POS_MIN)
    curlRightMiddle(POS_MIN)
    curlRightRing(POS_MIN)
    curlRightPinky(POS_MIN)

#Arm
def relaxLeftArm():
    turnLeftUnderarm(0)
    curlLeftEllbow(POS_MIN)
    turnLeftUperarm(0)

def relaxRightArm():
    turnRightUnderarm(0)
    curlRightEllbow(POS_MIN)
    turnRightUperarm(0)

def liftLeftArm():
    curlLeftEllbow(-2000)
    turnLeftShoulderVert(9000)

def liftRightArm():
    curlRightEllbow(-2000)
    turnRightShoulderVert(9000)

#Shoulder
def relaxLeftShoulder():
    turnLeftShoulderHor(POS_MIN)
    turnLeftShoulderVert(POS_MIN)

def relaxRightShoulder():
    turnRightShoulderHor(POS_MIN)
    turnRightShoulderVert(POS_MIN)

#Head
def relaxHead():
    turnHeadHor(0)
    turnHeadVert(0)

#---------------------------------------
# Medium part Movements
#---------------------------------------

def relaxFingers():
    relaxRightFingers()
    relaxLeftFingers()

def moveFingers(amount):
    moveLeftFingers(amount)
    moveRightFingers(amount)

def curlFingers():
    curlLeftFingers()
    curlRightFingers()

def relaxArms():
    relaxRightArm()
    relaxLeftArm()

def relaxShoulders():
    relaxLeftShoulder()
    relaxRightShoulder()


#---------------------------------------
# Positions Movements
#---------------------------------------

def relaxPos():
    relaxFingers()
    relaxShoulders()
    relaxHead()
    relaxArms()
    
def readyPos():
    moveFingers(3000)
    curlRightEllbow(-2000)
    curlLeftEllbow(-2000)


#---------------------------------------
# Save Shutdown
#---------------------------------------

def shutdown():
    relaxPos()

    for i in range(10):
        time.sleep(0.05)
        slh.set_enable(i,False)
        time.sleep(0.05)
        sah.set_enable(i,False)
        time.sleep(0.05)
        srh.set_enable(i,False)