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

    results = model.predict(frame, conf=0.25, device=0, verbose=False, iou=0.5)
    try:
     object_results = af.AuxiliaryFunctions(annotated_frame, results, model,labels,skeleton)
     object_results.GetResults()
    # results = model.predict(frame,conf = 0.3)
    # Visualize the results on the frame
     for r in results:
        # print(r.probs)
        # print(r.boxes)
        # print(r.keypoints)
        pass
        
    #all this on the cropped frame, so the coordinates are relative to the cropped frame; we will need to shift them back to the original frame coordinates later
     annotated_frame, alldata, box_data = object_results.GetImage() 
     del results #ADDD SILVIA
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


def adjust_alldata_for_x_offset(alldata, x_offset, scale=0.5):
    if not alldata:
        return alldata
    adjusted = []
    for i, v in enumerate(alldata):
        if i % 3 == 0:  # x coordinate
            try:
            
               # adjusted_val = (v + x_offset) * (1 / scale) if not pd.isna(v) else v
                #  to actual frame which was reduced 
                adjusted_val = (v + x_offset) * (1 / 1) if not pd.isna(v) else v
                adjusted.append(adjusted_val)
            except Exception:
                adjusted.append(v)
        else:
            adjusted.append(v)
    return adjusted


def adjust_box_data_for_x_offset(box_data, x_offset, scale=0.5):
    if not box_data or len(box_data) < 5:
        return box_data
    x, y, w, h, c = box_data
    try:
        #x = (x + x_offset) * (1 / scale) if not pd.isna(x) else x
        x = (x + x_offset) * (1 / 1) if not pd.isna(x) else x
    except Exception:
        pass
    return [x, y, w, h, c]


def process_video_frames(cap, out, models, labels, skeleton, modified_labels, crop_type='none', x_crop=None, frame_scale=0.5):
    """Process video frames through models and collect data."""
    rows0, rows0b = [], []
    rows1, rows1b = [], []
    frame_number = 1

    # x_crop is from original image; scale to current working frame size
    if x_crop is not None:
        if isinstance(x_crop, (list, tuple)):
            x_crop_resized = [int(float(v) * frame_scale) for v in x_crop]
        else:
            x_crop_resized = int(float(x_crop) * frame_scale)
    else:
        x_crop_resized = None

    stop = False
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, None, fx=frame_scale, fy=frame_scale, interpolation=cv2.INTER_AREA)
        annotated_frame = frame.copy()

        if crop_type in ['both', 'left', 'right']:
            crops = get_frame_crops(frame, crop_type, x_crop_resized)
            for crop_idx, (crop_frame, x_offset) in enumerate(crops):
                model = models[crop_idx] if crop_idx < len(models) else models[0]
                crop_annotated, alldata, box_data = AnalyzeFrame(crop_frame, crop_frame.copy(), model, labels, skeleton)

                # show the crop used for prediction
                cv2.imshow(f'Crop {crop_idx}', crop_annotated)

                # overlay crop annotations onto full frame
                x1 = x_offset
                x2 = x_offset + crop_annotated.shape[1]
                annotated_frame[:, x1:x2] = crop_annotated

                # coordinate shift and scale back to original frame
                alldata = adjust_alldata_for_x_offset(alldata, x_offset, frame_scale)
                box_data = adjust_box_data_for_x_offset(box_data, x_offset, frame_scale)

                if crop_type == 'left' and crop_idx == 0:
                    rows0.append(alldata); rows0b.append(box_data)
                elif crop_type == 'right' and crop_idx == 0:
                    rows1.append(alldata); rows1b.append(box_data)
                else:
                    if crop_idx == 0:
                        rows0.append(alldata); rows0b.append(box_data)
                    elif crop_idx == 1:
                        rows1.append(alldata); rows1b.append(box_data)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    stop = True
                    break
            if stop:
                break
        else:
            for index, model in enumerate(models):
                annotated_frame, alldata, box_data = AnalyzeFrame(frame, annotated_frame, model, labels, skeleton)
                # scale back to original frame coordinates
                alldata = adjust_alldata_for_x_offset(alldata, 0, frame_scale)
                box_data = adjust_box_data_for_x_offset(box_data, 0, frame_scale)
                if alldata and len(alldata) > 0:
                    if index == 0:
                        rows0.append(alldata); rows0b.append(box_data)
                    elif index == 1:
                        rows1.append(alldata); rows1b.append(box_data)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    stop = True
                    break
            if stop:
                break

        out.write(annotated_frame)
        
        frame_number += 1
        print(frame_number)

    return rows0, rows0b, rows1, rows1b


def export_to_excel(rows0, rows0b, rows1, rows1b, output_paths, modified_labels, labels_box):
    """Export collected data to Excel files."""
    sheet1 = 'BMR'
    sheet2 = 'BMR_box'
    
    df0 = pd.DataFrame(rows0, columns=modified_labels)
    df1 = pd.DataFrame(rows1, columns=modified_labels)
    df0b = pd.DataFrame(rows0b, columns=labels_box)
    df1b = pd.DataFrame(rows1b, columns=labels_box)
    
    df0.to_excel(output_paths['right'], sheet_name=sheet1)
    df0b.to_excel(output_paths['rightb'], sheet_name=sheet2)
    df1.to_excel(output_paths['left'], sheet_name=sheet1)
    df1b.to_excel(output_paths['leftb'], sheet_name=sheet2)


def main():
    selected_file = select_file_with_gui()
    config = load_configuration(selected_file)
    
    type_experiment = config['type_experiment']
    models = initialize_models(config['file_model'])
    labels, skeleton = setup_labels_and_skeleton(type_experiment)
    
    video_path = config['video_path']
    video_output = config['video_output']
    directory = os.path.dirname(video_output)
    filename = os.path.splitext(os.path.basename(video_output))[0]
    
    output_paths = setup_output_paths(directory, filename)
    modified_labels = modifylabels(labels)
    labels_box = ['BMR_x', 'BMR_y', 'width', 'height', 'conf']
    
    crop_type = config['side_to_track']
    x_crop = config['x_crop']
    frame_scale = 0.5

    cap, out, new_width, new_height = setup_video_writer(video_path, video_output, scale=frame_scale)
    rows0, rows0b, rows1, rows1b = process_video_frames(
        cap, out, models, labels, skeleton, modified_labels,
        crop_type=crop_type, x_crop=x_crop, frame_scale=frame_scale
    )
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    export_to_excel(rows0, rows0b, rows1, rows1b, output_paths, modified_labels, labels_box)


if __name__ == "__main__":
    main()