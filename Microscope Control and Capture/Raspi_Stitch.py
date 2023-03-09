# import cv2 library
import cv2
import numpy as np
import os

mylist = os.listdir('/Users/peter/Desktop/Python Microscope/image/')
mylist = np.array(mylist)
mylist.shape(2,1)

# read the images
img1 = cv2.imread('/Users/peter/Desktop/Python Microscope/image/IMG_2112 Large.jpeg')
img2 = cv2.imread('/Users/peter/Desktop/Python Microscope/image/IMG_2113 Large.jpeg')


def concat_vh(list_2d):
    
      # return final image
    return cv2.vconcat([cv2.hconcat(list_h) 
                        for list_h in list_2d])
  
# function calling
img_tile = concat_vh([[img1, img1, img2],
                      [img2, img1, img1],
                      [img2, img1, img2]])
# show the output image
cv2.imshow('concat_vh.jpg', img_tile)
cv2.waitKey(0)
 