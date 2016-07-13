"""this is pulled from Pololu's library for driving motors here: https://github.com/pololu/drv8835-motor-driver-rpi/blob/master/pololu_drv8835_rpi.py"""

import wiringpi2
import lcm
from butterbotlcm import motor_t


lc = lcm.LCM()
# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 480  # 19.2 MHz / 2 / 480 = 20 kHz
MAX_SPEED = _max_speed

io_initialized = False

A1IN = 0
A2IN = 2

B1IN = 3
B2IN = 4

def io_init():
  global io_initialized
  if io_initialized:
    return

  wiringpi2.wiringPiSetupGpio()
  wiringpi2.pinMode(A1IN, wiringpi2.GPIO.PWM_OUTPUT)
  wiringpi2.pinMode(B1IN, wiringpi2.GPIO.PWM_OUTPUT)

  wiringpi2.pwmSetMode(wiringpi2.GPIO.PWM_MODE_MS)
  wiringpi2.pwmSetRange(MAX_SPEED)
  wiringpi2.pwmSetClock(2)

  wiringpi2.pinMode(A2IN, wiringpi2.GPIO.OUTPUT)
  wiringpi2.pinMode(B2IN, wiringpi2.GPIO.OUTPUT)

  io_initialized = True

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

        wiringpi2.digitalWrite(self.dir_pin, dir_value)
        wiringpi2.pwmWrite(self.pwm_pin, speed)

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
