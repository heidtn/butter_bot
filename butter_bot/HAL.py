"""
Hardware abstraction layer for butterbot.  Allows access to the physical hardware as well as possible simulators

author: Nathan Heidt
"""
from RPIO import PWM

class RobotHAL:
	def __init__(self, hardware="BBB"):
		# Setup PWM and DMA channel 0
		PWM.setup()
		PWM.init_channel(0, 20000)
		self.motors = PWM.servo()
		


	def openGPIO(self):
		pass