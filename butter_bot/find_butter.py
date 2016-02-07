import cv2
import zbar
from PIL import Image

#takes an opencv image and returns the coordinates on screen (for now)
def findButter(image):
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')

	im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY,dstCn=0)
	pil = Image.fromarray(im)
	width, height = pil.size
	raw = pil.tobytes()
	image = zbar.Image(width, height, 'Y800', raw)
	scanner.scan(image)
	for symbol in image:
		print 'decoded', symbol.type, 'symbol', '"%s"' % repr(symbol.location)

	del image
