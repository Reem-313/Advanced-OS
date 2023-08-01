#-  File: pi_cam_capture.py
#-  Title: Pi camera photo taking App
#-  Description: An application to take photos with the pi's camera
#-  Usage: Run the script and provide with the environment variable
#          CAMERA_OUTPUT_DST of the location of the photo to be stored
#-  Author: Joshua-Yuill


# - Importing Libraries
from datetime import datetime
from pathlib import Path
import os

import cv2

from lib import logger

# - Logging Setup
logger.log_setup(5,str(Path(os.environ.get("LOGS_PATH","logs/"),"camera.log")))

# - Variables
name = datetime.now().isoformat()+".jpg"
location = os.environ.get("CAMERA_OUTPUT_DST")
width = os.environ.get("IMAGE_WIDTH","1920")
height = os.environ.get("IMAGE_HEIGHT","1080")
imagesStored = int(os.environ.get("STORED_IMAGE_COUNT","20"))
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L) # Setting the camera device
path = str(Path(location,name))

# - Error Checking
if location is None:
    print("No path set. Set Path. Exited")
    logger.log_critical("No path set. Set Path. Exited")
    exit(1)
    
# - Capture Taking
cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(width))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height))

ret, frame = cap.read()

cv2.imwrite(path, frame)

cap.release()
logger.log_notice(f"Capture Taken and saved to {path}")

# - Image Rotation
images = list(sorted(Path(location).glob("*.jpg")))

if len(images) > imagesStored:
    images = images[:len(images) - imagesStored]
        
    for iPath in images:
        iPath.unlink()


# - Sources
#Environment Variables (https://www.nylas.com/blog/making-use-of-environment-variables-in-python/)
#Pi Camera Integration In Python (https://picamera.readthedocs.io/en/release-1.13/)
#Iso8601 Time Format In Python (https://pynative.com/python-iso-8601-datetime/#:~:text=Format%20of%20ISO%208601%20Date,%2D18T11%3A40%3A22.519222.)
#Pi camera fix for ubuntu 20.04

