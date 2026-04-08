# -*- coding: utf-8 -*-
from ultralytics import YOLO

class Initialization:
    def __init__(self):
        # Load the YOLOv8 model
        self.model = YOLO('yolov8l.pt')
        # Open the video file
        self.video_path = "J:/TestDeeplearning/TestDeeplearning/M888.avi"
        # Threshold
        self.conf = 0.1
    def getVideoPath(self):
        return self.video_path