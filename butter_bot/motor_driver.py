"""this is pulled from Pololu's library for driving motors here: https://github.com/pololu/drv8835-motor-driver-rpi/blob/master/pololu_drv8835_rpi.py"""

from RPIO import PWM
import RPIO

import lcm
from butterbotlcm import motor_t


lc = lcm.LCM()


A1IN = 17
A2IN = 22
B1IN = 27
B2IN = 23

CHANNEL = 0
TIMING = 3000
MAX_SPEED = TIMING - 1

def io_init():
  PWM.setup()
  PWM.init_channel(CHANNEL, TIMING)
  RPIO.setmode(RPIO.BOARD)
  RPIO.setup(A1IN, RPIO.OUT)
  RPIO.setup(A2IN, RPIO.OUT)
  RPIO.setup(B1IN, RPIO.OUT)
  RPIO.setup(B2IN, RPIO.OUT)


class Motor(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin

    def setSpeed(self, speed):
        if speed < 0:
            speed = -speed
            dir_value = 1
        else:
            dir_value = 0

        if speed > MAX_SPEED:
            speed = MAX_SPEED

        RPIO.output(self.dir_pin, dir_value)
        PWM.add_channel_pulse(CHANNEL, self.pwm_pin, 0, speed)


class Motors(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        self.motor1 = Motor(A1IN, A2IN)
        self.motor2 = Motor(B1IN, B2IN)
        io_init()

    def setSpeeds(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

motors = Motors()

def my_handler(channel, data):
  msg = motor_t.decode(data)
  motors.setSpeeds(msg.leftmotor, msg.rightmotor)

if __name__ == "__main__":
  subscription = lc.subscribe("EXAMPLE", my_handler)
  try:
    while True:
      lc.handle()
  except KeyboardInterrupt:
    pass
