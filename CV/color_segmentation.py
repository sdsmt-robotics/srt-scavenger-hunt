import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from mpl_toolkits import mplot3d

img = cv.imread('hallway.jpg')
img_full = img.copy()
img = cv.resize(img,None,fx = 0.1,fy = 0.1,interpolation = cv.INTER_CUBIC)

img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
plt.imshow(img_rgb)
plt.show()

red_plane = img_hsv[:,:,0]
red_vector = red_plane.flatten()
green_plane = img_hsv[:,:,1]
green_vector = green_plane.flatten()
blue_plane = img_hsv[:,:,2]
blue_vector = blue_plane.flatten()

# blue bucket pixels
print("+==========Blue Bucket==========+")
bbpt1x = int(input('Pt 1 X: ')) #250
bbpt1y = int(input('Pt 1 Y: ')) #140

bbpt2x = int(input('Pt 2 X: ')) #350
bbpt2y = int(input('Pt 2 Y: ')) #250

bb_im = img_hsv[bbpt1y:bbpt2y, bbpt1x:bbpt2x,:]
rgb_rec = cv.rectangle(img_rgb, (bbpt1x, bbpt1y), (bbpt2x, bbpt2y), (0, 0, 255), 3)
bbrp = bb_im[:,:,0]
bbrpv = bbrp.flatten()
bbgp = bb_im[:,:,1]
bbgpv = bbgp.flatten()
bbbp = bb_im[:,:,2]
bbbpv = bbbp.flatten()

plt.imshow(rgb_rec)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(red_vector,green_vector,blue_vector,'k.', alpha = 0.005)
ax.plot3D(bbrpv,bbgpv,bbbpv,'b.',alpha = 0.1)
ax.set_xlabel('Hue')
ax.set_ylabel('Sat')
ax.set_zlabel('Value')
plt.show()

print("+==========Test Color Ranges==========+")
while (True):
	cont = input('Y/N: ')
	if (cont == 'N') or (cont == 'n'):
		break
	print("+==========Lower Parameters==========+")

	hl = int(input('H: ')) #111
	sl = int(input('S: ')) #102
	vl = int(input('V: ')) #86

	print("+==========Upper Parameters==========+")

	hu = int(input('H: ')) #120
	su = int(input('S: ')) #202
	vu = int(input('V: ')) #116

	fig = plt.figure()
	lower_vals = np.array([hl, sl, vl])
	upper_vals = np.array([hu, su, vu])
	# Threshold the image to get only blue bucket
	mask = cv.inRange(img_hsv, lower_vals, upper_vals)
	# Bitwise-AND mask and original image
	res = cv.bitwise_and(img_hsv,img_hsv, mask = mask)
	plt.imshow(res)

	plt.show()

