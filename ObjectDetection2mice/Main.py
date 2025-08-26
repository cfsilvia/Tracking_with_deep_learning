# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 15:48:53 2023

@author: Administrator
The idea is to get two animals from 2 different models
"""
import cv2
from ultralytics import YOLO
import AuxiliaryFunctions as af
import pandas as pd
from openpyxl.workbook import Workbook
import os
import yaml
import tkinter as tk
from tkinter import filedialog, messagebox
from Gui_auxiliary_app import select_file_with_gui


        

def AnalyzeFrame(frame,annotated_frame,model,labels,skeleton):
    # Run YOLOv8 inference on the frame
    results = model.predict(frame,conf = 0.01,workers = 0, device=0)#analyze without marking
   # results = model.predict(frame,workers = 0, device = 0)
    try:
     object_results = af.AuxiliaryFunctions(annotated_frame, results, model,labels,skeleton)
     object_results.GetResults()
    # results = model.predict(frame,conf = 0.3)
    # Visualize the results on the frame
     for r in results:
        print(r.probs)
        print(r.boxes)
        print(r.keypoints)
        
    #annotated_frame = results[0].plot()
     annotated_frame, alldata, box_data = object_results.GetImage()
    except:
      annotated_frame = annotated_frame
      alldata = [float('nan')]*3*len(labels)
      box_data = [float('nan')]*5
    return annotated_frame, alldata, box_data


def  modifylabels(labels):
    list = []
    for l in labels:
        list.append(l + '_x')
        list.append(l + '_y')
        list.append(l + '_score')
    
    return list



def main():
 
    selected_file = select_file_with_gui()
   
    
    with open(selected_file,'r') as file:
       data = yaml.safe_load(file)


    type_experiment = data['type_experiment']
    #values = ['Mice','Blind moles from the side','Blind moles from the top']  
    number_models = len(data['file_model'])
    Models = []
   #%%
    for n in range(number_models):
      file_model = data['file_model'][n]
      model = YOLO(file_model)
      Models.append(model) 
#Settings
# Load the YOLOv8 model
# model for the 2 blind moles  left and right
    # model1 = YOLO('F:/Juna/19_6_2024/yoloBlindmole_allbody_vs1/weights/best.pt')
    # model2 = YOLO('F:/Juna/19_6_2024/yoloBMR_left6/weights/best.pt') #left to do this
    
    # Models = [model1,model2]
    
# Open the video file
    video_path = data['video_path']
    video_output = data['video_output']
    
    #get path and filename
    # Get directory and filename
    directory = os.path.dirname(video_output)
    filename =os.path.splitext(os.path.basename(video_output))[0]
    
    
    #video_path = "F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT.avi"
    #video_output = "F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_2blind_moles_5.avi"
    #%%
    if type_experiment == 'mice':
       labels = ['center','ear_Left','ear_Right', 'hips_left', 'hips_right','nose', 'shoulders','tail_2','tail_Base','tail_End','tail_round'] 
       skeleton = [('nose','ear_Left'),('nose','ear_Right'),('nose','shoulders'),('shoulders','center'),('center','hips_left'),
                ('center','hips_right'),('center','tail_Base'),('tail_Base','tail_round'),('tail_round','tail_2')
                ,('tail_2','tail_End')]
    elif type_experiment == 'Blind moles from the side':
    
    # labels =  ['BM_snout','BM_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom', 'BM_head',
    #           'BM_centroid', 'BM_back', 'BM_rear_leg_1', 'BM_rear_leg_2', 'BM_front_leg_1', 'BM_front_leg_2']
    
   #for the  side        
        labels = ['BM_snout', 'BM_lower_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom', 
               'BM_head','BM_centroid', 'BM_back', 'BM_right_rear_leg_1', 'BM_left_rear_leg_1',
               'BM_right_front_leg_1','BM_left_front_leg_1','BM_behind', 'BM_low_behind', 'BM_below_mouth', 'BMR_Middle']
    #for side
        skeleton = [('BM_snout','BM_head'),('BM_head','BM_centroid'),('BM_centroid','BM_back'),('BM_back','BM_behind'),('BM_behind','BM_low_behind'),
                ('BM_snout','BM_below_mouth'),('BM_below_mouth','BM_left_front_leg_1'),('BM_left_front_leg_1','BM_right_front_leg_1'),
               ('BM_left_front_leg_1','BM_left_rear_leg_1'),('BM_left_rear_leg_1','BM_right_rear_leg_1'),('BM_snout','BM_ridge_bottom'),
                ('BM_ridge_bottom','BM_ridge_middle'),('BM_ridge_middle','BM_ridge_top')]
    
    
    elif type_experiment == 'Blind moles from the top':
    #for the up
         labels = ['BM_snout', 'BM_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom',
              'BM_head_right','BM_head_left', 'BM_right_front_leg', 'BM_left_front_leg',
             'BM_right_rear_leg','BM_left_rear_leg','BM_behind', 'BM_right_back', 'BM_left_back', 
              'BM_centroid_left', 'BM_centroid_right']
    
    #for up
         skeleton = [('BM_snout','BM_head_right'),('BM_snout','BM_head_left'),('BM_head_right','BM_centroid_right'),('BM_centroid_right','BM_right_back'),('BM_right_back','BM_behind'),
                 ('BM_behind','BM_left_back'),('BM_left_back','BM_centroid_left'),('BM_centroid_left','BM_head_left'),
                ( 'BM_right_front_leg', 'BM  _left_front_leg'),('BM_right_rear_leg','BM_left_rear_leg'),('BM_snout','BM_ridge_bottom'),
                 ('BM_ridge_bottom','BM_ridge_middle'),('BM_ridge_middle','BM_ridge_top'),('BM_snout','BM_mouth')]
    
   #%%
    labels = sorted(labels)
    # skeleton = [('BM_snout','BM_ridge_bottom'),('BM_ridge_bottom','BM_ridge_middle'),('BM_ridge_middle','BM_ridge_top'),
    #             ('BM_snout','BM_mouth'),('BM_snout','BM_head'),('BM_head','BM_centroid'),('BM_centroid','BM_back'),
    #             ('BM_snout','BM_front_leg_1'),('BM_rear_leg_1','BM_rear_leg_2'),('BM_front_leg_1','BM_front_leg_2'),
    #             ('BM_front_leg_1','BM_rear_leg_1'),('BM_front_leg_2','BM_rear_leg_2'),('BM_rear_leg_1','BM_back'),
    #             ('BM_mouth','BM_ridge_bottom')]
    
    #skeleton = [('BM_snout','BM_head'),('BM_head','BM_centroid'),('BM_snout','BM_front_leg_1'),('BM_front_leg_1', 'BM_front_leg_2')]
    #skeleton = [('BM_snout','BM_head'),('BM_snout','BM_front_leg_1'),('BM_front_leg_1', 'BM_front_leg_2'),('BM_head','BM_centroid'),('BM_centroid','BM_back')]
    
    
    
    excel_outputr = directory + '/' + filename + '_right.xlsx'
    excel_outputrb = directory + '/' + filename + '_rightb.xlsx'
    excel_outputl = directory + '/' + filename + '_left.xlsx'
    excel_outputlb = directory + '/' + filename + '_leftb.xlsx'
    
    # excel_outputr = "F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_right1.xlsx"
    # excel_outputrb = "F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_rightb1.xlsx"
    # excel_outputl = "F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_left1.xlsx"
    # excel_outputlb = "F:/Juna/19_6_2024/BMR2 vs BMR5 as stimulus 8.7.21_side_CUT_YOLO_leftb1.xlsx"
   # excel_output = "X:/Users/Members/Juna/BMR2 vs BMR5 as stimulus 8.7.21_up_yoloBMR_UP4.xlsx"
    
    #excel_output = "X:/Users/Members/Juna/BMR10 vs BMR6 as stimulus_26.6.22_side_allbody_vs0.xlsx"
   # excel_output1 = "F:/YaelShammaiData/AnnotationFromYael/C57 103-1mcut_Yolovs3_Black.xlsx"
    sheet1 = 'BMR'
    sheet2 = 'BMR_box'
    labels_box = ['BMR_x', 'BMR_y', 'width', 'height', 'conf']
    _if_Cropped = 1
  #  sheet2 = 'black mouse'
    
    modified_labels =  modifylabels(labels)
    
    df0 = pd.DataFrame(columns = modified_labels)
    df1 = pd.DataFrame(columns = modified_labels)
    
    df0b = pd.DataFrame(columns = labels_box)
    df1b = pd.DataFrame(columns = labels_box)
########
    cap = cv2.VideoCapture(video_path)
    # Get the frames per second (fps)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out = cv2.VideoWriter(video_output,cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))
    frame_number = 1
    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        #annotated_frame = frame.copy() #all the events will be copy here

        if success:
            #crop the image
            # Define the ROI (top-left corner and bottom-right corner)
            x_start, y_start = 0, 730  # Top-left corner
            x_end, y_end = 2000, 2000    # Bottom-right corner
            
            # if _if_Cropped == 1:
            #    cropped_image = frame[y_start:y_end, x_start:x_end]
            #    frame = cropped_image 
            #%%
            annotated_frame = frame.copy() #all the events will be copy here
            index =0
            for model in Models:
                
               annotated_frame, alldata, box_data = AnalyzeFrame(frame,annotated_frame,model,labels,skeleton)
               #add to a different data sheet
               #ADD
               
               if index == 0 and len(alldata)!=0: 
                 df0.loc[len(df0)] = alldata 
                 df0b.loc[len(df0b)] = box_data
               elif index == 1 and len(alldata)!=0 :
                  df1.loc[len(df1)] = alldata
                  df1b.loc[len(df1b)] = box_data 
               index +=1
               
        
                
            # Break the loop if 'q' is pressed
           
            # Display the annotated frame
            #cv2.imshow("YOLOv8 Inference", annotated_frame)
            out.write(annotated_frame)
            
            #cv2.waitKey(1) & 0xFF == ord("q"):
            #break
        else:
            # Break the loop if the end of the video is reached
            break
        frame_number += 1
        print(frame_number)
    #save data to excel
        #df0.to_excel(excel_output, sheet_name = sheet1)
        #df1.to_excel(excel_output1, sheet_name = sheet2)
    
    # Release the video capture object and close the display window
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    df0.to_excel(excel_outputr, sheet_name = sheet1)
    df0b.to_excel(excel_outputrb, sheet_name = sheet2)
    df1.to_excel(excel_outputl, sheet_name = sheet1)
    df1b.to_excel(excel_outputlb, sheet_name = sheet2)

if __name__ == "__main__":
    main() 