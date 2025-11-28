import random
import time
from logging import shutdown

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_servo_v2 import BrickletServoV2

# Replace with your Servo Bricklet 2.0 UID
UIDRightHand = '2b7m'
UIDArm = '2b7W'

# Create IP connection
ipcon = IPConnection()

# Create Servo Bricklet 2.0 object
servoRightHand = BrickletServoV2(UIDRightHand, ipcon)
servoArm = BrickletServoV2(UIDArm, ipcon)

# Connect to brickd
ipcon.connect('localhost', 4223)

curl = 9000
relax = -9000

def pause(amount = 0.01):
    time.sleep(amount)

def turnRightThumb(amount):
    servoRightHand.set_position(0, amount)

def curlRightThumb(amount):
    amount *= (-1)
    servoRightHand.set_position(1, amount)

def curlRightIndex(amount):
    amount *= (-1)
    servoRightHand.set_position(2, amount)

def curlRightMiddle(amount):
    servoRightHand.set_position(3, amount)

def curlRightRing(amount):
    servoRightHand.set_position(4, amount)

def curlRightPinky(amount):
    amount *= (-1)
    servoRightHand.set_position(5, amount)

def liftArm():
    servoArm.set_position(9, -7000)
    pause()
    servoRightHand.set_position(8, 2000)

def turnArm(amount):
    servoRightHand.set_position(7,amount)

def relaxArm():
    servoArm.set_position(9,relax)
    pause()
    servoRightHand.set_position(8, curl)

def moveAllFingers(amount):
    turnRightThumb(amount)
    pause()
    curlRightThumb(amount)
    pause()
    curlRightIndex(amount)
    pause()
    curlRightMiddle(amount)
    pause()
    curlRightRing(amount)
    pause()
    curlRightPinky(amount)

def italianHand():
    turnRightThumb(curl)
    pause()
    curlRightThumb(0)
    pause()
    curlRightIndex(4000)
    pause()
    curlRightMiddle(5000)
    pause()
    curlRightRing(5000)
    pause()
    curlRightPinky(8000)

def italianMove():
    servoRightHand.set_position(8, -1000)
    pause(0.5)
    servoRightHand.set_position(8, 1000)



servoRightHand.set_pulse_width(0, 1200, 2470)
servoRightHand.set_pulse_width(8, 1200, 2470)
servoArm.set_pulse_width(9,570,2470)

pause()
x = 1
while x <= 8:
    servoRightHand.set_pulse_width(x, 530, 2470)
    pause()
    x += 1
x = 0
while x <= 8:
    servoRightHand.set_enable(x, True)
    pause()
    x += 1

servoArm.set_enable(9, True)
servoRightHand.set_enable(8, True)
print("initialisation completed")

print("lift Arm")
liftArm()
pause()
turnArm(7000)
time.sleep(1)


print('Italian')
italianHand()
pause(1)

i=0
while i <= 5:
    italianMove()
    pause(0.5)
    i+=1

print("shutting down")
time.sleep(3)
relaxArm()
pause()
turnArm(0)
pause()
moveAllFingers(relax)
time.sleep(3)

y = 0
while y <=  9:
    servoRightHand.set_enable(y, False)
    pause()
    y += 1

servoArm.set_enable(9,False)
print("all done")

ipcon.disconnect()
