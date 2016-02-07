import sys
sys.path.append("..")
import find_butter
import cv2

cap = cv2.VideoCapture(0)

while True:
	ret, im = cap.read()
	cv2.imshow('frame', im)
	find_butter.findButter(im)
	if cv2.waitKey(1) & 0xFF == 32:
		break

cv2.destroyAllWindows()
cap.release()
