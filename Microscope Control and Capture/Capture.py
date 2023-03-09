import cv2 as cv
import numpy as np
import os
import Raspi_Stage_Control as RSC

# Index camera and open window
capture = cv.VideoCapture(0)
cv.namedWindow("Mobile Microscope V2")
scan_number = 0
dirname = "/Users/peter/Desktop/Python Microscope/image"

# Read frames from video capture
while True: #Begin while loop if feed is coming in from the camera
    ret, frame = capture.read()
    if not ret:
        print("Failed to read frame")
        break
    cv.imshow("Mobile Microscope V2", frame)

    #Allow window to open and remain open until key is pressed 27=escape key 32= space key
    k = cv.waitKey(1) & 0xFF
    if k%256 == 27:
        print("Escape hit, closing the window")
        break
    if k%256 == 32:
        print("Space bar hit, taking a picture")
        image_name = "TB_SSM_Scan_{}.jpg".format(scan_number)
        cv.imwrite(os.path.join(dirname, image_name), frame) 
        scan_number += 1
    if k == ord('x'):
        RSC.translate_axis('x')
    if k == ord('y'):
        RSC.translate_axis('y')
    
    
capture.release()

cv.destroyAllWindows()