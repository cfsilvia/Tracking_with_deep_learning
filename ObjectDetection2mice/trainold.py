# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 09:28:43 2023

@author: Administrator
"""
import cv2
from ultralytics import YOLO
import torch
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import polars as pl
from ultralytics.engine.trainer import BaseTrainer



'''
Auxiliary functions

'''

def select_file(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title = message)
    return file_path


def get_input():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Ask the user for input
    user_input = simpledialog.askstring("Input", "Please give a name to your model \n as BM_right_YOLO_7_8_2025:")
    
    return user_input

#%%
file_path = select_file('Select the configuration file (conf_pose.yaml)')

model_name = get_input()

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# #Set up GPU
device = "0" if torch.cuda.is_available() else "cpu"
if device == "0":
    torch.cuda.set_device(0)
print("Device:",device)

# Load  a pretained  YOLOv8 model
#model = YOLO('yolov8l.pt')
model = YOLO('yolov8l-pose.pt')

#model.train(data='F:/YaelShammaiData/Roboflow/conf.yaml', epochs=500, name = 'yoloRNew',workers = 0,patience=0)  # train the model
#model.train(data='F:/YaelShammaiData/data/conf_box_1.yaml', epochs=500, name = 'yoloG', workers = 0,patience=0)  # train the model
#model.train(data='F:/YaelShammaiData/dataPose/conf_pose.yaml', epochs=500, name = 'yoloPoseA', workers = 0,patience=0)  # train the model
#model.train(data='F:/YaelShammaiData/dataPoseWhite/conf_pose.yaml', epochs=500, name = 'yoloPoseWhiteVs2', workers = 0,patience=0)  # train the 

#model.train(data='F:/RagadData/Data/conf_box_1.yaml', epochs=500, name = 'yoloSimilarMice', workers = 0,patience=0)  # train the model

#model.train(data='F:/YaelShammaiData/AnnotationFromYael/conf_pose.yaml', epochs=500, name = 'yoloPoseWhiteNew', workers = 0,patience=0)  # train the

#model.train(data='F:/Juna/19_6_2024/TrainingDataSecondmouse/conf_pose.yaml', epochs=500, name = 'yoloBMR_Left',project='F:/Juna/models', workers = 0,patience=0)  # train the  
#addition 
BaseTrainer.read_results_csv = lambda self: pl.read_csv(self.csv, infer_schema_length=10000, ignore_errors=True).to_dict(as_series=False)


model.train(data = file_path, epochs=500, name = model_name ,project='U:/LabSoftware/ModelsForTracking_Deep_Learning', workers = 0,patience=0)  # train the  