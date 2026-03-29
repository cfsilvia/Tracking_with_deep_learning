import os
import pandas as pd
import numpy as np

def load_labels_files(folder, num_frames, labels, shape_stack,Path_Folder,shapes = None):
    """
    Loads keypoints from YOLO-style label files with visibility.
    Falls back to default grid keypoints if files are missing.
    """
    points = []
    labels_all = []
    files_found = False
    box = []
    #Read the saved order of keypoint from test2 file
    saved_labels_order = read_labels(Path_Folder)
    saved_labels_order = add_visibility_labels(saved_labels_order)
    

    for frame_idx in range(0,num_frames):
        label_file = os.path.join(folder, f"{frame_idx + 1}_image.txt")
        if os.path.exists(label_file):
            files_found = True
            with open(label_file, 'r') as f:
                coords = open_split(f)
                box = get_bounding_box(coords, shape_stack, frame_idx, box, shapes)
                points, labels_all = get_labels(coords, labels, shape_stack, frame_idx, points, labels_all, saved_labels_order,shapes)

        else:
            continue
    return box, points, labels_all

def read_labels(Path_Folder):
    df = pd.read_csv(Path_Folder + '//test2.csv')
    saved_labels = df.columns
    return saved_labels

def open_split(f):
    line = f.readline().strip()
    parts = line.split(' ')[1:]  # skip class id 
    coords = [float(p) for p in parts]

    return coords

def get_bounding_box(coords, shape_stack, frame_idx, box, shapes = None):
    x_cn, y_cn, wn, hn = coords[:4]
    w = wn * shapes[frame_idx][1]
    h= hn * shapes[frame_idx][0]
    x_c = x_cn * shapes[frame_idx][1]
    y_c = y_cn * shapes[frame_idx][0]
    
    
    x1 = x_c - w / 2
    x2 = x_c + w / 2
    y1 = y_c - h / 2
    y2 = y_c + h / 2

    box.append([
            [frame_idx, y1, x1],
            [frame_idx, y1, x2],
            [frame_idx, y2, x2],
            [frame_idx, y2, x1]
        ])
    
    return box
    



def get_labels(coords, labels, shape_stack, frame_idx, points, labels_all, saved_labels,shapes = None):
    
    for l in labels:
        #find the original labels i the saved ones
        positions = []
        for i, col in enumerate(saved_labels): 
            if  l in col:
                positions.append(i-1)
                
        x = coords[positions[0]] * shapes[frame_idx][1]  # width
        y = coords[positions[1]] * shapes[frame_idx][0]  # height

         # convert (0,0) to NaN
        if x == 0 and y == 0:
            x, y = np.nan, np.nan

        points.append([frame_idx, y, x])
        labels_all. append(l)
    return points, labels_all
    
def add_visibility_labels(saved_labels_ordered):
    new_labels = []
    # keep the first 5 elements as-is
    new_labels.extend(saved_labels_ordered[:5])
    
    for i in range(5, len(saved_labels_ordered), 2):
        x_label = saved_labels_ordered[i]
        y_label = saved_labels_ordered[i + 1]
        
        base_name = x_label.split(' (')[0]
        v_label = base_name + ' (v)'
        
        new_labels.extend([x_label, y_label, v_label])
    
    return new_labels