import time

class PID:
	def __init__(self, P, I, D):
		self.kP = P
		self.kI = I
		self.kD = D

		self.isClipped = True
		self.clip = 40.0

		self.previous = 0.0
		self.previousTime = time.time()

		self.isFirst = True

	def setClip(self, clip, isClipped):
		self.isClipped = isClipped
		self.clip = abs(clip)

	def update(newVal, goal):
		error = newVal - goal

		if self.isFirst:
			self.previous = error
			self.isFirst = False

		curtime = time.time()
		timedif = (curtime - self.previousTime())

		P = self.kP*(error)
		D = self.kD*(error - self.previous)*(timedif)
		I += self.kI*(error)*(timedif)

		I = clip(I)

		self.previousTime = time.time()
		self.previous = error

		return P + I + D

	def clip(self, I):
		if I > self.clip:
			I = self.clip
		elif I < -self.clip:
			I = -self.clip
		return I
