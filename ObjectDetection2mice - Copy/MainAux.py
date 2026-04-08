# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 13:52:38 2023

@author: Administrator
"""
import torch
from ultralytics import YOLO
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import cv2

R = np.array(np.arange(96, 256, 32))
G = np.roll(R, 1)
B = np.roll(R, 2)

COLOR_IDS = np.array(np.meshgrid(R, G, B)).T.reshape(-1, 3)

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
  # draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
  #            (left, top)],
  #           width=thickness,
  #           fill=color)
  # Green color in BGR
  # Annotate the image with the bounding box.
  #color = tuple(COLOR_IDS[class_id % len(COLOR_IDS)].tolist())[::-1]
  color = (0, 0, 255)
  image = cv2.rectangle(image, (left, top), (right, bottom), color, thickness)
  # cv2.line(image, (left, top), (left, bottom), color, thickness) 
  # cv2.line(image, (left, bottom), (right, bottom), color, thickness) 
  # cv2.line(image,(right, bottom), (right, top), color, thickness) 
  # cv2.line(image, (right, top),(left, top), color, thickness) 
  
  font = cv2.FONT_HERSHEY_SIMPLEX
  fontScale = 0.5
  thickness = 2
  text = class_id + " " + str(conf)
  size, _ = cv2.getTextSize(text, font, fontScale, thickness)
  width, height = size
  cv2.putText(image,text,(left,top - height),font,fontScale,color,thickness)
 
  overlay = image.copy()
  overlay = cv2.rectangle(overlay, (left, top ), (left + width, top - 2*height), color, -1)
  alpha = 0.4  # Transparency factor.

# Following line overlays transparent rectangle over the image
  cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0,image)
  
  # # If the total height of the display strings added to the top of the bounding
  # # box exceeds the top of the image, stack the strings below the bounding box
  # # instead of above.
  # display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
  # # Each display_str has a top and bottom margin of 0.05x.
  # total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

  # if top > total_display_str_height:
  #   text_bottom = top
  # else:
  #   text_bottom = top + total_display_str_height
  # # Reverse list and print from bottom to top.
  # for display_str in display_str_list[::-1]:
  #   text_width, text_height = font.getsize(display_str)
  #   margin = np.ceil(0.05 * text_height)
  #   draw.rectangle([(left, text_bottom - text_height - 2 * margin),
  #                   (left + text_width, text_bottom)],
  #                  fill=color)
  #   draw.text((left + margin, text_bottom - text_height - margin),
  #             display_str,
  #             fill="black",
  #             font=font)
  #   text_bottom -= text_height - 2 * margin
  display_image(image)   
    
    


path = "J://TestDeeplearning//TestDeeplearning//Twomice.jpg"

model = YOLO("yolov8l.pt")
results = model.predict(path,conf = 0.05)
result = results[0]
box = result.boxes[3]

cords = box.xyxy[0].tolist()
cords = [round(x) for x in cords]
class_id = result.names[box.cls[0].item()]
conf = round(box.conf[0].item(), 2)
print("Object type:", class_id)
print("Coordinates:", cords)
print("Probability:", conf)

image = cv2.imread(path)
draw_bounding_box_on_image(image,
                               cords,
                               'blue',4,class_id,conf)



box = result.boxes[1]

cords = box.xyxy[0].tolist()
cords = [round(x) for x in cords]
class_id = result.names[box.cls[0].item()]
conf = round(box.conf[0].item(), 2)
print("Object type:", class_id)
print("Coordinates:", cords)
print("Probability:", conf)

#image = cv2.imread(path)
draw_bounding_box_on_image(image,
                               cords,
                               'blue',
                               4,class_id,conf)

cv2.imwrite("J://TestDeeplearning//TestDeeplearning//Twomice2.jpg",image)


