# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 09:12:13 2023

@author: Administrator
"""

#for tracking 

import cv2
from ultralytics import YOLO
import torch



import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# Load the YOLOv8 model
model = YOLO('C:/Users/Administrator/runs/detect/yoloSimilarMice/weights/best.pt')

# Open the video file
video_path = "F:/RagadData/31-10-2023/for_tracking.avi"
video_output = "F:/RagadData/31-10-2023/for_tracking_yolov3.avi"
cap = cv2.VideoCapture(video_path)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter(video_output,cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, conf = 0.3, iou = 0.5,tracker="F:/RagadData/31-10-2023/botsort.yaml")

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
       # cv2.imshow("YOLOv8 Tracking", annotated_frame)
        out.write(annotated_frame)
        # Break the loop if 'q' is pressedeeeeeeeee
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()