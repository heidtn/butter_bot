"""this is pulled from Pololu's library for driving motors here: https://github.com/pololu/drv8835-motor-driver-rpi/blob/master/pololu_drv8835_rpi.py"""

from RPIO import PWM
import RPIO

import lcm
from butterbotlcm import motor_t


lc = lcm.LCM()


A1IN = 17
A2IN = 27

B2IN = 23
B1IN = 22

TIMING = 2000
MAX_SPEED = TIMING - 1

def io_init():
  PWM.setup()
  PWM.set_loglevel(PWM.LOG_LEVEL_ERRORS)

class Motor(object):
    def __init__(self, xin1, xin2, channels):
        self.xin1 = xin1
        self.xin2 = xin2
	self.channel1 = channels[0]
	self.channel2 = channels[1]
	PWM.init_channel(self.channel1)
	PWM.init_channel(self.channel2)

    def setSpeed(self, speed):
	speed = int(speed/100.0 * MAX_SPEED + 0.5)
        if speed < 0:
            speed = -speed
            dir_value = 1
        else:
            dir_value = 0

        if speed > MAX_SPEED:
            speed = MAX_SPEED
        
        PWM.add_channel_pulse(self.channel1, self.xin1, 0, dir_value*speed)
        PWM.add_channel_pulse(self.channel2, self.xin2, 0, (1 - dir_value)*speed)


class Motors(object):
    def __init__(self):
        try:
            io_init()
        except RuntimeError:
            print("Already configured IO")
    
        self.motor1 = Motor(A1IN, A2IN, (0, 1))
        self.motor2 = Motor(B1IN, B2IN, (2, 3))
    
    def __del__(self):
        RPIO.cleanup()

    def setSpeeds(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

motors = Motors()

def my_handler(channel, data):
  msg = motor_t.decode(data)
  motors.setSpeeds(msg.leftmotor, msg.rightmotor)

if __name__ == "__main__":
  subscription = lc.subscribe("BUTTERBOT_MOTOR", my_handler)
  try:
    while True:
      lc.handle()
  except KeyboardInterrupt:
    pass
