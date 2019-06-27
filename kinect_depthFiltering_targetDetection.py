from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

def nothing(x):
    pass
# Create trackbar windows
cv2.namedWindow('Value selector')
cv2.createTrackbar('Min value','Value selector',0,1000,nothing)
cv2.createTrackbar('Max value','Value selector',1000,1000,nothing)

# Kinect runtime object (communicates with kinect) 
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
time.sleep(3)

while True:
    # Get next depth frame, if it exists
    if kinect.has_new_depth_frame():
        # Get frame from sensor, reshape as __________________________
        depthFrame = kinect.get_last_depth_frame()
        depthImageData = np.reshape(depthFrame,(424,512,-1))
        depthImageRGB = cv2.cvtColor(depthImageData, cv2.COLOR_GRAY2RGB).astype(np.uint8)
        depthFrame = None

        # Get trackbar info
        minVal = cv2.getTrackbarPos('Min value','Value selector')
        maxVal = cv2.getTrackbarPos('Max value','Value selector')

        # Filter using hsv threshold
        filterdDepthImage = cv2.inRange(depthImageData,np.array(minVal),np.array(maxVal))

        # Find contours and keep only square
        cont,hierarchy = cv2.findContours(filterdDepthImage.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        num_cont = len(cont)
        if num_cont>0:
            cont = sorted(cont, key = cv2.contourArea, reverse = True)
            # loop over the contours
            for c in cont:
                # approximate the contour
                per = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.1*per, True)
                # check number of points of contour
                if len(approx) == 4:
                    cv2.drawContours(depthImageRGB, [approx], -1, (0,255,0), 2)
                    mom = cv2.moments(approx)
                    if mom['m00'] != 0:
                        x = int(mom['m10']/mom['m00'])
                        y = int(mom['m01']/mom['m00'])
                    cv2.circle(depthImageRGB, (x,y), 2, (0,255,0), -1)
                    depthPoint = PyKinectV2._DepthSpacePoint(x,y)
                    cameraPoint = kinect._mapper.MapDepthPointToCameraSpace(depthPoint, depthImageData[y,x])
                    print("X: ",cameraPoint.x," Y: ",cameraPoint.y," Z: ",cameraPoint.z)
                    break

        # Draw frame using opencv
        cv2.imshow('Depth image',depthImageRGB)
        key = cv2.waitKey(1)
        if key == 27:
            break

        # Draw frame using opencv
        cv2.imshow('Filtered depth image',filterdDepthImage)
        key = cv2.waitKey(1)
        if key == 27:
            break

    # Time delay
    time.sleep(.03)

# Close the Kinect sensor, close the image window
kinect.close()
cv2.destroyAllWindows()