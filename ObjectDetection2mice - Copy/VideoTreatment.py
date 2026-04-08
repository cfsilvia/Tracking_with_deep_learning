# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 16:25:08 2023

@author: Administrator
"""

import cv2
from Initialization import Initialization

class VideoTreatment(Initialization):
    def Applymodel(self):
        cap = cv2.VideoCapture(self.getVideoPath())
        

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLOv8 inference on the frame
                results = model(frame)

                

                # Display the annotated frame
                cv2.imshow("YOLOv8 Inference", annotated_frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Break the loop if the end of the video is reached
                break

        # Release the video capture object and close the display window
        cap.release()
        cv2.destroyAllWindows()