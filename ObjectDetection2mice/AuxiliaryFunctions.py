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


#COLORS = [(255,248,240),(255, 0, 0), (0, 0, 139),(30, 105, 210), (180, 105, 255),(47, 255, 173)]
COLORS = [(8,104,172),(204,76,2),(65,174,118),(206,18,86),(129,15,124),(231,41,138),(255,255,204),(150,150,150),(35,132,67),
          (166,189,219),(127,39,4),(0,0,0),(199,233,180),(217,72,1),(129,15,124),(2,129,138)]

class AuxiliaryFunctions:
    def __init__(self, image, results,model,labels,skeleton):
        self._image = image
        self._results = results
        self._model = model
        self._labels = labels #original labels
        self._skeleton = skeleton # how the points are combined
        self._finalList = []
        self._box_inf = []
        
        
    def GetResults(self):
        result = self._results #take first
        for r in result: #loop through each class
           box = r.boxes
           
           b = box[0] # boxes for each class -take the box with better probability

           cords = b.xyxy[0].tolist()
           cords = [round(x) for x in cords]
           keypoints = r.keypoints.xy[0].tolist()
           conf_score = r.keypoints.conf[0].tolist()
         
           class_id = r.names[b.cls[0].item()]
           conf = round(b.conf[0].item(), 2)
           print("Object type:", class_id)
          # print("Coordinates:", cords)
           #print("Probability:", conf)
           print(keypoints)
           print(conf_score)
           
           self._finalList = FusionData(keypoints,conf_score)
           
           #add box information
           self._box_inf = cords
           self._box_inf.append(conf)

           if class_id == 'black':
                     color = (0,0,255)
           else:
                     color = (255,0,0)
                     
       # self._image = draw_bounding_box_on_image(self._image, cords, color, 4, class_id, conf)
        self._image = add_points_on_image(self._image, keypoints)
       # cv2.imshow("YOLOv8 Inference", self._image)
        self._image = add_skeleton_on_image(self._image, keypoints,self._labels,self._skeleton)
       # cv2.imshow("YOLOv8 Inference", self._image)

    def GetImage(self):
        return self._image,self._finalList, self._box_inf
        
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