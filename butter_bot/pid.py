import time

class PID:
	def __init__(self, P, I, D):
		self.kP = P
		self.kI = I
		self.kD = D

		self.P = 0
		self.I = 0
		self.D = 0

		self.isClipped = True
		self.clip = 40.0

		self.previous = 0.0
		self.previousTime = time.time()

		self.isFirst = True

	def setClip(self, clip, isClipped):
		self.isClipped = isClipped
		self.clip = abs(clip)

	def update(self, newVal, goal):
		error = newVal - goal

		if self.isFirst:
			self.previous = error
			self.isFirst = False

		curtime = time.time()
		timedif = curtime - self.previousTime

		self.P = self.kP*(error)
		self.D = self.kD*(error - self.previous)*(timedif)
		self.I += self.kI*(error)*(timedif)

		self.I = self.clipVal(self.I)

		self.previousTime = time.time()
		self.previous = error

		return self.P + self.I + self.D

	def clipVal(self, I):
		if I > self.clip:
			I = self.clip
		elif I < -self.clip:
			I = -self.clip
		return I
