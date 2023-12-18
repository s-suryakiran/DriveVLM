import cv2
import os
import glob

# Define the path to the directory containing the images
image_folder = "IMAGES_FOLDER"
video_name = 'output_video.mp4'

# Find all the images in the directory. Adjust the pattern as per your file type.
images = [img for img in sorted(glob.glob(f"{image_folder}/*.png"))]

# Determine the width and height from the first image
frame = cv2.imread(images[0])
height, width, layers = frame.shape

# Define the codec and create VideoWriter object (using mp4v for MP4 format)
video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

# Loop through all images and add them to the video
for image in images:
    video.write(cv2.imread(image))

cv2.destroyAllWindows()
video.release()