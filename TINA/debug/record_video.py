# Python program to save a
# video using OpenCV


import cv2


# Create an object to read
# from camera
video = cv2.VideoCapture(0)

# We need to check if camera
# is opened previously or not
if (video.isOpened() == False):
	print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.

scale = 0.3
frame_width = int(video.get(3) * scale)
frame_height = int(video.get(4) * scale)

size = (frame_width, frame_height)

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.
result = cv2.VideoWriter('production_02.avi',
						cv2.VideoWriter_fourcc(*'MJPG'),
						1, size)
print("Video has started")

while(True):
	ret, frame = video.read()
	frame = cv2.resize(frame,None,fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)

	if ret == True:

		# Write the frame into the
		# file 'filename.avi'
		result.write(frame)

		# Display the frame
		# saved in the file
		#cv2.imshow('Frame', frame)

		# Press S on keyboard
		# to stop the process
		if cv2.waitKey(1) & 0xFF == ord('s'):
			break

	# Break the loop
	else:
		break

# When everything done, release
# the video capture and video
# write objects
video.release()
result.release()

# Closes all the frames
cv2.destroyAllWindows()

print("The video was successfully saved")

