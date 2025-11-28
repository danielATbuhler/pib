import piblib.movements as m
import time

# Shake hand
def shakeHand():
    m.srh.set_motion_configuration(8, 30000, 40000, 40000)
    m.liftRightArm()
    time.sleep(2)
    m.moveRightFingers(9000)
    time.sleep(2)
    for i in range(5):
        time.sleep(0.5)
        m.curlRightEllbow(-3000)
        time.sleep(0.5)
        m.curlRightEllbow(0)
    m.relaxRightFingers()
    time.sleep(4)
    m.relaxRightArm()
    m.stdSettings()
