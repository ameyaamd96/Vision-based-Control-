# The packages used are imported in the next few lines.
# pikinect2 is a Python wrapper that allows python to access the Kinect SDK files. See following link:
#	https://github.com/Kinect/PyKinect2
# numpy is a popular package for matrix manipulation
#	http://www.numpy.org/
# cv2 is the "OpenCV" computer vision library
#	https://opencv.org/
# time is a standard python library that helps with timing functions
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
import time

# The following lines create trackbar windows to easily adjust HSV values 
def nothing(x):
    pass
# Create trackbar windows
cv2.namedWindow('Tracking')
cv2.createTrackbar('hmin','Tracking',100,255,nothing)
cv2.createTrackbar('hmax','Tracking',255,255,nothing)
cv2.createTrackbar('smin','Tracking',0,255,nothing)
cv2.createTrackbar('smax','Tracking',255,255,nothing)
cv2.createTrackbar('vmin','Tracking',82,255,nothing)
cv2.createTrackbar('vmax','Tracking',255,255,nothing)

# Kinect runtime object (communicates with kinect, uses PyKinectV2)
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
time.sleep(3)

# Loop through kinect frames forever
while True:
    # Get next color frame, if it exists
    if kinect.has_new_color_frame():
        # Get frame from sensor, reshape as BGRA matrix
        colorFrame = kinect.get_last_color_frame()	# Raw camera data in vector form
        colorImageBGRA = np.reshape(colorFrame,(1080,1920,-1)).astype(np.uint8) # Reshape camera data to matrix form
        colorImageBGR = cv2.cvtColor(colorImageBGRA, cv2.COLOR_BGRA2BGR) # Remove alpha channel from data
        hsv_image = cv2.cvtColor(colorImageBGRA,cv2.COLOR_BGR2HSV) # Convert BGR (blue-green-red) data to HSV (hue-saturation-value) data 
        colorFrame = None # delete camera data in preparation for next frame

        # Get trackbar info, user sets minimum and maximum HSV filtering values
        hmin = cv2.getTrackbarPos('hmin','Tracking')
        hmax = cv2.getTrackbarPos('hmax','Tracking')
        smin = cv2.getTrackbarPos('smin','Tracking')
        smax = cv2.getTrackbarPos('smax','Tracking')
        vmin = cv2.getTrackbarPos('vmin','Tracking')
        vmax = cv2.getTrackbarPos('vmax','Tracking')

        # Filter image using HSV threshold values
		# Pixels that DO NOT fall within the user-selected HSV value range are set to value of 0
		# Pixels that DO fall within the user-selected HSV value range are set to value of 1
        h,s,v = cv2.split(hsv_image) # Splits the HSV matrix into separate H, S, V matrices
        hf = cv2.inRange(h,np.array(hmin),np.array(hmax))	# Filters H matrix
        sf = cv2.inRange(s,np.array(smin),np.array(smax))	# Filters S matrix
        vf = cv2.inRange(v,np.array(vmin),np.array(vmax))	# Filters V matrix
        filteredImage = cv2.bitwise_and(hf, cv2.bitwise_and(sf,vf))	# Creates matrix of 1's and 0's according to filtering

        # Display original color frame using opencv
        cv2.imshow('Color image',colorImageBGR)
        # The following lines are routine and needed whenever imshow is used (they don't matter too much)
		# They simply allow for user keyboard input after a window is shown
	 
        
        # Display filtered frame using opencv
		# Pixels that fall within the HSV range are shown in white, all other pixels are black
        cv2.imshow('Filtered color image',filteredImage)
        key = cv2.waitKey(1)
        if key == 27:
            break

    # Time delay between frames
    time.sleep(.1)
# Close the Kinect sensor, close the image window (these lines never get called since the loop runs forever)
#kinect.close()
#cv2.destroyAllWindows()
#