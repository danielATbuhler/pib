import time
from logging import shutdown

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_servo_v2 import BrickletServoV2

curlFinger = 9000
relaxFinger = (-9000)
sleep = 0.01

def turnLeftThumb(amount):
    servo.set_position(0, amount)

def curlLeftThumb(amount):
    servo.set_position(1, amount)

def curlLeftIndex(amount):
    amount *= (-1)
    servo.set_position(2, amount)

def curlLeftMiddle(amount):
    servo.set_position(3, amount)

def curlLeftRing(amount):
    amount *= (-1)
    servo.set_position(4, amount)

def curlLeftPinky(amount):
    amount *= (-1)
    servo.set_position(5, amount)

def moveAllFingers(amount):
#    turnLeftThumb(amount)
    time.sleep(sleep)
    curlLeftThumb(amount)
    time.sleep(sleep)
    curlLeftIndex(amount)
    time.sleep(sleep)
    curlLeftMiddle(amount)
    time.sleep(sleep)
    curlLeftRing(amount)
    time.sleep(sleep)
    curlLeftPinky(amount)

def makeFist():
    print("start relax makefist")
    moveAllFingers(relaxFinger)
    time.sleep(sleep)
    print("makefist")
    moveAllFingers(curlFinger)
    print("Fist end")

def makeScissors():
    curlLeftThumb(curlFinger)
    curlLeftRing(curlFinger)
    curlLeftPinky(curlFinger)

def makePaper():
    moveAllFingers(-9000)
    turnLeftThumb(-9000)

# Replace with your Servo Bricklet 2.0 UID
UID = '2b83'

# Create IP connection
ipcon = IPConnection()

# Create Servo Bricklet 2.0 object
servo = BrickletServoV2(UID, ipcon)

# Connect to brickd
ipcon.connect('localhost', 4223)

servo.set_pulse_width(0, 1200, 2470)
time.sleep(sleep)
x = 1
while x <= 5:
    servo.set_pulse_width(x, 530, 2470)
    time.sleep(sleep)
    x += 1
x = 0
while x <= 5:
    servo.set_enable(x, True)
    time.sleep(sleep)
    x += 1
print("initialisation completed")

makeFist()
time.sleep(3)
print("next")
moveAllFingers(relaxFinger)
makeScissors()

print("shutting down")
time.sleep(3)
moveAllFingers(relaxFinger)

y = 0
while y <=  9:
    servo.set_enable(y, False)
    time.sleep(sleep)
    y += 1

print("all done")

ipcon.disconnect()
