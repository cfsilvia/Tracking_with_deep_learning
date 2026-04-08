# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 08:44:03 2023

@author: Administrator
"""

'''
Auxiliary Functions to draw results
'''
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated
import torch
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

COLORS = [
    (31, 119, 180),
    (255, 127, 14),
    (44, 160, 44),
    (214, 39, 40),
    (148, 103, 189),
    (140, 86, 75),
    (227, 119, 194),
    (127, 127, 127),
    (188, 189, 34),
    (23, 190, 207),
    (254, 178, 76),
    (156, 102, 31),
    (165, 42, 42),
    (255, 237, 160),
    (84, 48, 5),
    (0, 0, 0),
    (253, 191, 111),
    (255, 255, 255),
    (230, 85, 13),
    (173, 221, 142),
    (158, 188, 218),
]
#COLORS = [(255,248,240),(255, 0, 0), (0, 0, 139),(30, 105, 210), (180, 105, 255),(47, 255, 173)]
#COLORS = [(8,104,172),(204,76,2),(65,174,118),(206,18,86),(129,15,124),(231,41,138),(255,255,204),(150,150,150),(35,132,67),
#          (166,189,219),(127,39,4),(0,0,0),(199,233,180),(217,72,1),(129,15,124),(2,129,138)]

class AuxiliaryFunctions:
    def __init__(self, image, results,model,labels,skeleton,x_divider):
        self._image = image
        self._results = results
        self._model = model
        self._labels = labels #original labels
        self._skeleton = skeleton # how the points are combined
        self._finalList = []
        self._box_inf = []
        self._x_divider = x_divider
        
        
    def GetResults(self):
        detections = []
        for r in self._results:
            for i, box in enumerate(r.boxes):
                conf = box.conf[0].item()
                cords = box.xyxy[0].tolist()
                cords = [float(x) for x in cords]
                center_x = (cords[0] + cords[2]) / 2
                detections.append({
                    'box': box,
                    'keypoints': r.keypoints.xy[i],
                    'conf_score': r.keypoints.conf[i],
                    'class_id': r.names[box.cls[0].item()],
                    'box_conf': conf,
                    'cords': cords,
                    'center_x': center_x
                })
        
        # Separate into left and right
        left_detections = [d for d in detections if d['center_x'] < self._x_divider]
        right_detections = [d for d in detections if d['center_x'] >= self._x_divider]
        
        # Select best for each side if conf > 0.6
        self._left_finalList = []
        self._left_box_inf = []
        if left_detections:
            best_left = max(left_detections, key=lambda x: x['box_conf'])
            if best_left['box_conf'] > 0.1:
                keypoints = best_left['keypoints'].tolist()
                conf_score = best_left['conf_score'].tolist()
                cords = best_left['cords'] + [best_left['box_conf']]
                self._left_finalList = FusionData(keypoints, conf_score)
                self._left_box_inf = cords
                self._image = add_points_on_image(self._image, keypoints)
                self._image = add_skeleton_on_image(self._image, keypoints, self._labels, self._skeleton)
        
        self._right_finalList = []
        self._right_box_inf = []
        if right_detections:
            best_right = max(right_detections, key=lambda x: x['box_conf'])
            if best_right['box_conf'] > 0.6:
                keypoints = best_right['keypoints'].tolist()
                conf_score = best_right['conf_score'].tolist()
                cords = best_right['cords'] + [best_right['box_conf']]
                self._right_finalList = FusionData(keypoints, conf_score)
                self._right_box_inf = cords
                self._image = add_points_on_image(self._image, keypoints)
                self._image = add_skeleton_on_image(self._image, keypoints, self._labels, self._skeleton)

    def GetImage(self):
        return self._image, self._left_finalList, self._left_box_inf, self._right_finalList, self._right_box_inf
        
#############
'''
Auxiliiary functions
'''
def display_image(image):
  fig = plt.figure()
  plt.grid(False)
  plt.axis(False)
  plt.imshow(image)
  
  
def draw_bounding_box_on_image(image,
                               Coordinates,
                               color,
                               thickness,class_id,conf):
  """Adds a bounding box to an image."""
 # draw = ImageDraw.Draw(image)
  #im_width, im_height = image.size
  im_width = 1;
  im_height = 1;
  xmin = Coordinates[0]
  ymin = Coordinates[1]
  xmax = Coordinates[2]
  ymax = Coordinates[3]
  
  (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                ymin * im_height, ymax * im_height)

  image = cv2.rectangle(image, (left, top), (right, bottom), color, thickness)

  
  font = cv2.FONT_HERSHEY_SIMPLEX
  fontScale = 2
  thickness = 3
  text = class_id + " " + str(conf)
  size, _ = cv2.getTextSize(text, font, fontScale, thickness)
  width, height = size
  cv2.putText(image,text,(left,top - height),font,fontScale,color,thickness)
 
  overlay = image.copy()
  overlay = cv2.rectangle(overlay, (left, top ), (left + width, top - 2*height), color, -1)
  alpha = 0.2  # Transparency factor.

# Following line overlays transparent rectangle over the image
  cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0,image)
  
 
 # display_image(image)   
#  cv2.imshow("test",image)
  return image

''' add keypoints on the image'''

def add_points_on_image(image, keypoints):
    index =0
    overlay = image.copy()
    for k in keypoints:
      color_r = COLORS[index]
      x = k[0]
      y = k[1]
      center = (int(x),int(y))
      if center[0] == 0 and center[1] == 0:
          print("not draw keypoint")
      else:
         cv2.circle(overlay,center, radius = 6, color = color_r, thickness = -1) #it was 10
      
      index += 1
    plt.imshow(overlay)
    return overlay

def add_skeleton_on_image(image, keypoints,labels, skeleton):
        
        skeleton_numeric = ConvertLabelsToNumbers(labels,skeleton)
        
        for s in  skeleton_numeric:
            point1 = (int((keypoints[s[0]])[0]), int((keypoints[s[0]])[1]))
            point2 = (int((keypoints[s[1]])[0]), int((keypoints[s[1]])[1]))
            if (point1[0] == 0 and point1[1] == 0) or (point2[0] == 0 and point2[1] == 0):
                print("no skeleton")
            else:
                cv2.line(image,point1,point2,color = (0,255,255)) #draw the line
        # point1 = (int((keypoints[0])[0]), int((keypoints[0])[1])) #center
        # point2 = (int((keypoints[1])[0]), int((keypoints[1])[1])) #ear left
        # point3 = (int((keypoints[2])[0]), int((keypoints[2])[1])) #ear right
        # point4 = (int((keypoints[3])[0]), int((keypoints[3])[1])) #nose
        # point5 = (int((keypoints[4])[0]), int((keypoints[4])[1])) #tail
        #  #
        # cv2.line(image,point4,point1,color = (0,255,255))
        # cv2.line(image,point4,point2,color = (0,255,255))
        # cv2.line(image,point4,point3,color = (0,255,255))
        # cv2.line(image,point1,point5,color = (0,255,255))
       
        
        return image
    
def ConvertLabelsToNumbers(labels,skeleton):
    numbers = []
    
    for l in skeleton: #go through each tuple
       #find number in the list of first term
       print(l)
       index1 =labels.index(l[0])
       index2 =labels.index(l[1])
       numbers.append((index1,index2))
       
    
    return numbers



def FusionData(keypoints,conf_score):
    index = 0
    list = []
    for k in keypoints:
         k.append(conf_score[index])
         list.extend(k)
         index+=1
        
    return list