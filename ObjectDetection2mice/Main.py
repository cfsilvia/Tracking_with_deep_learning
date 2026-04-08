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


        

def AnalyzeFrame(frame,annotated_frame,model,labels,skeleton, x_crop):
    # Apply CLAHE for contrast enhancement
    # lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    # frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Run YOLOv8 inference on the frame
    # results = model.predict(frame,conf = 0.01,workers = 0, device=0)#analyze without marking
   # results = model.predict(frame,workers = 0, device = 0)
    #results = model.predict(frame, conf=0.25, device=0, verbose=False)
    #before prediction add to  each frame contrast enhancement

     results = model.predict(frame, conf=0.1, device=0, verbose=False, iou=0.5)
   # results = model.predict(frame, conf=0.01, device=0, verbose=False)
    #results = model.track(frame, conf=0.1, device=0, verbose=False, iou=0.5, persist=True)
    try:
     object_results = af.AuxiliaryFunctions(annotated_frame, results, model,labels,skeleton, x_crop)
     object_results.GetResults()
    # results = model.predict(frame,conf = 0.3)
    # Visualize the results on the frame
     for r in results:
        # print(r.probs)
        # print(r.boxes)
        # print(r.keypoints)
        pass
        
     annotated_frame, left_alldata, left_box_data, right_alldata, right_box_data = object_results.GetImage() 
     del results #ADDD SILVIA
    except:
      annotated_frame = annotated_frame
      left_alldata = [float('nan')] * (len(labels) * 3)
      left_box_data = [float('nan')] * 5
      right_alldata = [float('nan')] * (len(labels) * 3)
      right_box_data = [float('nan')] * 5
    return annotated_frame, left_alldata, left_box_data, right_alldata, right_box_data


def  modifylabels(labels):
    list = []
    for l in labels:
        list.append(l + '_x')
        list.append(l + '_y')
        list.append(l + '_score')
    
    return list



def load_configuration(selected_file):
    """Load configuration from YAML file."""
    with open(selected_file, 'r') as file:
        return yaml.safe_load(file)


def initialize_models(file_paths):
    """Initialize YOLO models from file paths."""
    return [YOLO(file_path) for file_path in file_paths]


def setup_labels_and_skeleton(type_experiment):
    """Setup labels and skeleton based on experiment type."""
    if type_experiment == 'mice':
        labels = ['center', 'ear_Left', 'ear_Right', 'hips_left', 'hips_right', 'nose', 
                  'shoulders', 'tail_2', 'tail_Base', 'tail_End', 'tail_round']
        skeleton = [('nose', 'ear_Left'), ('nose', 'ear_Right'), ('nose', 'shoulders'),
                   ('shoulders', 'center'), ('center', 'hips_left'), ('center', 'hips_right'),
                   ('center', 'tail_Base'), ('tail_Base', 'tail_round'), ('tail_round', 'tail_2'),
                   ('tail_2', 'tail_End')]
    elif type_experiment == 'Blind moles from the side':
        labels = ['BM_snout', 'BM_lower_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom',
                 'BM_head', 'BM_centroid', 'BM_back', 'BM_right_rear_leg_1', 'BM_left_rear_leg_1',
                 'BM_right_front_leg_1', 'BM_left_front_leg_1', 'BM_behind', 'BM_low_behind',
                 'BM_below_mouth', 'BMR_Middle']
        skeleton = [('BM_snout', 'BM_head'), ('BM_head', 'BM_centroid'), ('BM_centroid', 'BM_back'),
                   ('BM_back', 'BM_behind'), ('BM_behind', 'BM_low_behind'), ('BM_snout', 'BM_below_mouth'),
                   ('BM_below_mouth', 'BM_left_front_leg_1'), ('BM_left_front_leg_1', 'BM_right_front_leg_1'),
                   ('BM_left_front_leg_1', 'BM_left_rear_leg_1'), ('BM_left_rear_leg_1', 'BM_right_rear_leg_1'),
                   ('BM_snout', 'BM_ridge_bottom'), ('BM_ridge_bottom', 'BM_ridge_middle'),
                   ('BM_ridge_middle', 'BM_ridge_top')]
    elif type_experiment == 'Blind moles from the top':
        labels = ['BM_right_snout', 'BM_center_snout', 'BM_left_snout', 'BM_mouth', 'BM_right_ridge',
                 'BM_left_ridge', 'BM_right_ear', 'BM_left_ear', 'BM_left_forelimb', 'BM_right_forelimb',
                 'BM_left_hindlimb', 'BM_right_hindlimb', 'BM_pelvic_base', 'BM_right_side',
                 'BM_left_side', 'BM_centr', 'BM_left_hip', 'BM_right_hip']
        skeleton = [('BM_right_snout', 'BM_left_snout'), ('BM_left_snout', 'BM_center_snout'),
                   ('BM_center_snout', 'BM_right_snout'), ('BM_right_hip', 'BM_pelvic_base'),
                   ('BM_left_hip', 'BM_pelvic_base'), ('BM_pelvic_base', 'BM_centr'),
                   ('BM_right_ear', 'BM_right_side'), ('BM_right_side', 'BM_right_hip'),
                   ('BM_left_ear', 'BM_left_side'), ('BM_left_side', 'BM_left_hip'),
                   ('BM_center_snout', 'BM_right_ear'), ('BM_center_snout', 'BM_left_ear'),
                   ('BM_right_snout', 'BM_right_ridge'), ('BM_left_snout', 'BM_left_ridge')]
    
    return sorted(labels), skeleton


def setup_output_paths(directory, filename):
    """Setup output file paths."""
    return {
        'right': directory + '/' + filename + '_right.xlsx',
        'rightb': directory + '/' + filename + '_rightb.xlsx',
        'left': directory + '/' + filename + '_left.xlsx',
        'leftb': directory + '/' + filename + '_leftb.xlsx'
    }


def setup_video_writer(video_path, video_output, scale=0.5):
    """Setup video capture and writer objects."""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    new_width = int(frame_width * scale)
    new_height = int(frame_height * scale)
    
    out = cv2.VideoWriter(video_output, cv2.VideoWriter_fourcc(*'mp4v'), fps, (new_width, new_height))
    
    return cap, out, new_width, new_height


def get_frame_crops(frame, crop_type, x_crop):
    frame_w = frame.shape[1]
    if x_crop is None:
        cut_left = frame_w // 2
        cut_right = cut_left
    elif isinstance(x_crop, (list, tuple)) and len(x_crop) == 2:
        cut_left = int(x_crop[0])
        cut_right = int(x_crop[1])
    else:
        cut_left = int(x_crop)
        cut_right = cut_left

    cut_left = max(0, min(cut_left, frame_w))
    cut_right = max(0, min(cut_right, frame_w))
    if cut_right < cut_left:
        cut_right = cut_left

    if crop_type == 'left':
        return [(frame[:, :cut_left], 0)]
    if crop_type == 'right':
        return [(frame[:, cut_right:], cut_right)]
    return [(frame[:, :cut_left], 0), (frame[:, cut_right:], cut_right)]




def process_video_frames(cap, out, models, labels, skeleton, modified_labels, frame_scale=0.5,x_divider = None):
    """Process video frames through models and collect data."""
    rows_left, rows_leftb = [], []
    rows_right, rows_rightb = [], []
    frame_number = 1

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, None, fx=frame_scale, fy=frame_scale, interpolation=cv2.INTER_AREA)
        annotated_frame = frame.copy()

        for index, model in enumerate(models):
            annotated_frame, left_alldata, left_box_data, right_alldata, right_box_data = AnalyzeFrame(frame, annotated_frame, model, labels, skeleton, int(x_divider*frame_scale))
            
            rows_left.append(left_alldata)
            rows_leftb.append(left_box_data)
            rows_right.append(right_alldata)
            rows_rightb.append(right_box_data)

        out.write(annotated_frame)
        # cv2.imshow('Annotated Frame', annotated_frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        frame_number += 1
        print(frame_number)

    return rows_left, rows_leftb, rows_right, rows_rightb


def export_to_excel(rows_left, rows_leftb, rows_right, rows_rightb, output_paths, modified_labels, labels_box):
    """Export collected data to Excel files."""
    sheet1 = 'BMR'
    sheet2 = 'BMR_box'
    
    df_left = pd.DataFrame(rows_left, columns=modified_labels)
    df_right = pd.DataFrame(rows_right, columns=modified_labels)
    df_leftb = pd.DataFrame(rows_leftb, columns=labels_box)
    df_rightb = pd.DataFrame(rows_rightb, columns=labels_box)
    
    df_left.to_excel(output_paths['left'], sheet_name=sheet1)
    df_leftb.to_excel(output_paths['leftb'], sheet_name=sheet2)
    df_right.to_excel(output_paths['right'], sheet_name=sheet1)
    df_rightb.to_excel(output_paths['rightb'], sheet_name=sheet2)


def main():
    selected_file = select_file_with_gui()
    config = load_configuration(selected_file)
    
    type_experiment = config['type_experiment']
    models = initialize_models(config['file_model'])
    labels, skeleton = setup_labels_and_skeleton(type_experiment)
    
    video_path = config['video_path']
    video_output = config['video_output']
    x_divider = config['x_divider']
    directory = os.path.dirname(video_output)
    filename = os.path.splitext(os.path.basename(video_output))[0]
    
    output_paths = setup_output_paths(directory, filename)
    modified_labels = modifylabels(labels)
    labels_box = ['BMR_x', 'BMR_y', 'width', 'height', 'conf']
    
    # 
    frame_scale = 0.5

    cap, out, new_width, new_height = setup_video_writer(video_path, video_output, scale=frame_scale)
    rows_left, rows_leftb, rows_right, rows_rightb = process_video_frames(
        cap, out, models, labels, skeleton, modified_labels,  frame_scale = frame_scale, x_divider = x_divider
    )
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    export_to_excel(rows_left, rows_leftb, rows_right, rows_rightb, output_paths, modified_labels, labels_box)


if __name__ == "__main__":
    main()