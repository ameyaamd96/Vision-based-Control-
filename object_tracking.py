from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2
import time

def read_rgb_image(image_name, show):
 #   rgb_image = cv2.imread(image_name)
    if show: 
        cv2.imshow("RGB Image",image_name)
        rgb_image = image_name
    return rgb_image

def filter_color(rgb_image, lower_bound_color, upper_bound_color):
    #convert the image into the HSV color space
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv image",hsv_image)

    #find the upper and lower bounds of the yellow color (tennis ball)
    yellowLower =(30, 150, 100)
    yellowUpper = (50, 255, 255)

    #define a mask using the lower and upper bounds of the yellow color 
    mask = cv2.inRange(hsv_image, lower_bound_color, upper_bound_color)

    return mask

def getContours(binary_image):      
    #_, contours, hierarchy = cv2.findContours(binary_image, 
    #                                          cv2.RETR_TREE, 
    #                                           cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(binary_image.copy(), 
                                            cv2.RETR_EXTERNAL,
	                                        cv2.CHAIN_APPROX_SIMPLE)
    return contours


def draw_ball_contour(binary_image, rgb_image, contours):
    black_image = np.zeros([binary_image.shape[0], binary_image.shape[1],3],'uint8')
    
    for c in contours:
        area = cv2.contourArea(c)
        perimeter= cv2.arcLength(c, True)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if (area>100):
            cv2.drawContours(rgb_image, [c], -1, (150,250,150), 1)
            cv2.drawContours(black_image, [c], -1, (150,250,150), 1)
            cx, cy = get_contour_center(c)
            cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(black_image, (cx,cy),(int)(radius),(0,0,255),1)
            cv2.circle(black_image, (cx,cy),5,(150,150,255),-1)
            print ("Area: {}, Perimeter: {}".format(area, perimeter))
    print ("number of contours: {}".format(len(contours)))
    cv2.imshow("RGB Image Contours",rgb_image)
    cv2.imshow("Black Image Contours",black_image)

def get_contour_center(contour):
    M = cv2.moments(contour)
    cx=-1
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    return cx, cy

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
time.sleep(3)

#def main():
#    image_name = "images/tennisball05.jpg"
#    yellowLower =(30, 150, 100)
#    yellowUpper = (50, 255, 255)
#    rgb_image = read_rgb_image(image_name, True)
#    binary_image_mask = filter_color(rgb_image, yellowLower, yellowUpper)
#    contours = getContours(binary_image_mask)
#    draw_ball_contour(binary_image_mask, rgb_image,contours)

#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

#if __name__ == '__main__':
#    main()



#cv2.waitKey(0)
#cv2.destroyAllWindows()

while True:
    # Get next color frame, if it exists
    if kinect.has_new_color_frame():
        # Get frame from sensor, reshape as BGRA matrix
        raw_image = kinect.get_last_color_frame()	# Raw camera data in vector form
        image_nameBGRA = np.reshape(raw_image,(1080,1920,-1)).astype(np.uint8) # Reshape camera data to matrix form
        image_name = cv2.cvtColor(image_nameBGRA, cv2.COLOR_BGRA2BGR) # Remove alpha channel from data
        yellowLower =(30, 150, 100)
        yellowUpper = (50, 255, 255)
        rgb_image = read_rgb_image(image_name, True)
        binary_image_mask = filter_color(image_name, yellowLower, yellowUpper)
        contours = getContours(binary_image_mask)
        draw_ball_contour(binary_image_mask, rgb_image,contours)
        image_name = None # delete camera data in preparation for next frame
        key = cv2.waitKey(1)
        if key == 27:
            break

    # Time delay between frames
    time.sleep(.1)