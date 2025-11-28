import random
import time
from logging import shutdown

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_servo_v2 import BrickletServoV2

# Replace with your Servo Bricklet 2.0 UID
UIDLeftHand = '2b83'
UIDArm = '2b7W'

# Create IP connection
ipcon = IPConnection()

# Create Servo Bricklet 2.0 object
servoLeftHand = BrickletServoV2(UIDLeftHand, ipcon)
servoArm = BrickletServoV2(UIDArm, ipcon)

# Connect to brick
ipcon.connect('localhost', 4223)

curl = 9000
relax = (-9000)

def pause(amount = 0.01):
    time.sleep(amount)

def liftArm():
    servoArm.set_position(1, 2000)
    pause()
    servoLeftHand.set_position(8, 3000)

def relaxArm():
    servoArm.set_position(1,curl)
    pause()
    servoLeftHand.set_position(8,curl)

def turnLeftThumb(amount):
    servoLeftHand.set_position(0, amount)

def curlLeftThumb(amount):
    servoLeftHand.set_position(1, amount)

def curlLeftIndex(amount):
    amount *= (-1)
    servoLeftHand.set_position(2, amount)

def curlLeftMiddle(amount):
    servoLeftHand.set_position(3, amount)

def curlLeftRing(amount):
    amount *= (-1)
    servoLeftHand.set_position(4, amount)

def curlLeftPinky(amount):
    amount *= (-1)
    servoLeftHand.set_position(5, amount)

def moveAllFingers(amount):
#    turnLeftThumb(amount)
    pause()
    curlLeftThumb(amount)
    pause()
    curlLeftIndex(amount)
    pause()
    curlLeftMiddle(amount)
    pause()
    curlLeftRing(amount)
    pause()
    curlLeftPinky(amount)

def btwMove():
    servoLeftHand.set_position(7,-3500)
    moveAllFingers(3000)
    pause()
    servoLeftHand.set_position(8,-2000)
    pause(0.5)
    servoLeftHand.set_position(8,4000)
    pause(0.5)
    servoLeftHand.set_position(8, -2000)
    pause(0.5)
    servoLeftHand.set_position(8,4000)
    pause(0.5)
    servoLeftHand.set_position(8, -2000)
    pause(0.5)
    servoLeftHand.set_position(8, 3000)
    servoLeftHand.set_position(7, 0)


def makeFist():
    moveAllFingers(relax)
    pause()
    moveAllFingers(curl)

def makeScissors():
    curlLeftIndex(relax)
    curlLeftMiddle(relax)
    curlLeftThumb(curl)
    curlLeftRing(curl)
    curlLeftPinky(curl)

def makePaper():
    moveAllFingers(-9000)
    turnLeftThumb(-9000)

def makeMove():
    moveNumb = random.randint(1,3)
    print(moveNumb)
    if moveNumb == 1:
        print('fist')
        makeFist()
        pause()
    elif moveNumb == 2:
        print('Scissors')
        makeScissors()
        pause()
    else:
        print('Paper')
        makePaper()
        pause()

servoLeftHand.set_pulse_width(0, 1200, 2470)
servoLeftHand.set_pulse_width(7, 530,2470)
servoLeftHand.set_pulse_width(8, 1200,2470)
servoArm.set_pulse_width(1,1000,2470)

pause()
x = 1
while x <= 5:
    servoLeftHand.set_pulse_width(x, 530, 2470)
    pause()
    x += 1
x = 0
while x <= 9:
    servoLeftHand.set_enable(x, True)
    pause()
    x += 1

servoArm.set_enable(1, True)
servoLeftHand.set_enable(8, True)
print("initialisation completed")

print("lift Arm")
liftArm()
time.sleep(1)

btwMove()
pause()
makeMove()
pause()



print("shutting down")
time.sleep(3)
moveAllFingers(relax)
relaxArm()
time.sleep(3)

y = 0
while y <=  9:
    servoLeftHand.set_enable(y, False)
    pause()
    y += 1

servoArm.set_enable(1,False)
print("all done")

ipcon.disconnect()
