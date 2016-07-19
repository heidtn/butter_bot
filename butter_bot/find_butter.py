import subprocess
import sys, os, signal
import lcm

from butterbotlcm import tagpos_t
import time

from threading import Thread, Lock

#black part of tag size in meters
tagsize = .05
mutex = Lock()



#positions is of type tagpos
def findButter(positions):
	lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")

	command = ['tags/apriltags/build/bin/rpitags -d -S ' + str(tagsize)]
	
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
	
	global child_pid
	child_pid = process.pid

	# Poll process for new output until finished
	while True:
		nextline = process.stdout.readline()
		if nextline == '' and process.poll() != None:
			break

		if "Id" in nextline:
			ididx = nextline.index(')')
			line = nextline[(ididx + 1):]
			line = line.strip()
			elements = line.split(',')
			elements = map(lambda x: float(x.split('=')[1].replace('m', '')), elements)

			print elements

			mutex.acquire()
			try:
				positions.settag(elements[0], elements[1], elements[2], elements[3], elements[4], elements[5], elements[6])
				msg = tagpos_t()
				msg.timestamp = int(time.time())
				msg.dist = positions.dist
				msg.x = positions.x
				msg.y = positions.y
				msg.z = positions.z
				msg.roll = positions.roll
				msg.pitch = positions.pitch
				msg.yaw = positions.yaw
				lc.publish("BUTTERBOT", msg.encode())
			finally:
				mutex.release()

#this sounds pretty bad...
def kill_child():
	try:
		if child_pid is None:
			pass
		else:
			print "killing camera process"
			os.kill(child_pid, signal.SIGTERM)
	except Exception:
		print "process never started..."

import atexit
atexit.register(kill_child)

			

class Tagpos:
	def __init__(self):
		self.timestamp = time.time()
		self.dist = 0.0
		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		self.yaw = 0.0
		self.pitch = 0.0
		self.roll = 0.0

	def settag(self, dist, x, y, z, yaw, pitch, roll):
		self.dist = dist
		self.x = x
		self.y = y
		self.z = z
		self.yaw = yaw
		self.pitch = pitch
		self.roll = roll
		self.timestamp = time.time()


if __name__ == "__main__":
	dummy = Tagpos()
	findButter(dummy)
