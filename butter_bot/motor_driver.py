"""this is pulled from Pololu's library for driving motors here: https://github.com/pololu/drv8835-motor-driver-rpi/blob/master/pololu_drv8835_rpi.py"""

import wiringpi2


# Motor speeds for this library are specified as numbers
# between -MAX_SPEED and MAX_SPEED, inclusive.
_max_speed = 480  # 19.2 MHz / 2 / 480 = 20 kHz
MAX_SPEED = _max_speed

io_initialized = False
def io_init():
  global io_initialized
  if io_initialized:
    return

  wiringpi2.wiringPiSetupGpio()
  wiringpi2.pinMode(17, wiringpi2.GPIO.PWM_OUTPUT)
  wiringpi2.pinMode(27, wiringpi2.GPIO.PWM_OUTPUT)

  wiringpi2.pwmSetMode(wiringpi2.GPIO.PWM_MODE_MS)
  wiringpi2.pwmSetRange(MAX_SPEED)
  wiringpi2.pwmSetClock(2)

  wiringpi2.pinMode(22, wiringpi2.GPIO.OUTPUT)
  wiringpi2.pinMode(23, wiringpi2.GPIO.OUTPUT)

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

        io_init()
        wiringpi2.digitalWrite(self.dir_pin, dir_value)
        wiringpi2.pwmWrite(self.pwm_pin, speed)

class Motors(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        self.motor1 = Motor(12, 5)
        self.motor2 = Motor(13, 6)

    def setSpeeds(self, m1_speed, m2_speed):
        self.motor1.setSpeed(m1_speed)
        self.motor2.setSpeed(m2_speed)

motors = Motors()


if __name__ == "__main__":
	import time
	motors.setSpeeds(0, 0)
	time.sleep(1)
	motors.setSpeeds(100, 100)
	time.sleep(1)
	motors.setSpeeds(0, 0)
