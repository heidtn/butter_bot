import speech_recognition as sr
import cv2
import subprocess
import sys
import state_singleton as state

 


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
			curstate = "search_for_butter"
		elif "you pass butter" in words and curstate == "inquisition":
			say("ohmygod")
			curstate = "existential_crisis"
		else:
			print("not in dictionary")
			
	except sr.UnknownValueError:
		print("didn't catch that..." + repr(sys.exc_info()[0]))


def setupSpeech():
	r = sr.Recognizer()
	m = sr.Microphone()

	with m as source: r.adjust_for_ambient_noise(source)
	stop_listening = r.listen_in_background(m, speechCallback)


def main():
	global curstate
	curstate = "waiting"


	print("Initializing butterbot")
	print("Initializing speech module")
	setupSpeech()
	print("setup success")
	print("initializing camera module")

	say("purpose")
	curstate = "inquisition"
	print curstate


	while True:
		if curstate == "waiting":
			pass
		elif curstate == "inquisition":
			pass
		elif curstate == "search_for_butter":
			pass
		elif curstate == "go_to_butter":
			pass
		elif curstate == "grab_butter":
			pass
		elif curstate == "return_butter":
			pass
		elif curstate == "existential_crisis":
			pass		

if __name__=="__main__":
	main()
