import os
import cv2
import stitching

image_folder_path = "/Users/peter/Desktop/Python Microscope/image"
image_file_names = os.listdir(image_folder_path)

stitcher = stitching.Stitcher()
stitched_image = stitcher.stitch(image_file_names)

cv2.imwrite(os.path.join(image_folder_path, "stitched_image.jpg"), stitched_image)

cv2.imshow(stitched_image)
cv2.waitKey(0)
