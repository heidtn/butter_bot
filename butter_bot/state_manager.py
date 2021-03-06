import speech_recognition as sr
import lcm
import subprocess
import sys

from butterbotlcm import state_t

curstate = "idle"
lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")

import time

def say(phrase):
	if phrase == "purpose":
		subprocess.Popen(['mpg123', 'resources/whatismypurpose.mp3'])
	elif phrase == "ohmygod":
		subprocess.Popen(['mpg123', 'resources/ohmygod.mp3'])

def getState():
	return curstate

def speechCallback(recognizer, audio):
	try:
		curstate = getState()
		print curstate
		words = recognizer.recognize_google(audio)
		print("butterbot heard " + words)
		if "pass the butter" in words and curstate == "inquisition":
			updateState("get_butter")
		elif "you pass butter" in words and curstate == "inquisition":
			say("ohmygod")
			updateState("existential_crisis")
		else:
			print("not in dictionary, or bad state")
			
	except sr.UnknownValueError:
		print("didn't catch that..." + repr(sys.exc_info()[0]))


def setupSpeech():
	r = sr.Recognizer()
	m = sr.Microphone()
	print("opened Microphone")

	with m as source: r.adjust_for_ambient_noise(source)
	stop_listening = r.listen_in_background(m, speechCallback)

def updateState(newState):
	global curstate
	curstate = newState
	msg = state_t()
	msg.timestamp = int(time.time())
	msg.state = newState
	lc.publish("BUTTERBOT_STATE", msg.encode())


if __name__ == "__main__":
	global curstate
	print("Initializing speech module")
	setupSpeech()
	say("purpose")
	updateState("inquisition")
	print curstate

	while True:
		time.sleep(1)
		updateState(curstate)
		if curstate == "idle":
			pass
		elif curstate == "inquisition":
			pass
		elif curstate == "get_butter":
			pass
		elif curstate == "existential_crisis":
			pass		