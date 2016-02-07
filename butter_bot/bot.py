import speech_recognition as sr
import cv2

curstate = "waiting"




def speechCallback(recognizer, audio):
	try:
		words = recognizer.recognize_google(audio)
		print("butterbot heard " + words)
		if words.contains("pass the butter") and curstate == "inquisition":
			curstate = "search_for_butter"
		elif words.contains("you pass butter") and curstate == "inquisition":
			curstate = "existential_crisis"
			
	except LookupError:
		print("didn't catch that...")


def setupSpeech():
	r = sr.Recognizer()
	m = sr.Microphone()

	with m as source: r.adjust_for_ambient_noise(source)
	stop_listening = r.listen_in_background(m, speechCallback)


def main():
	print("Initializing butterbot")
	print("Initializing speech module")
	setupSpeech()
	print("setup success")
	print("initializing camera module")
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
