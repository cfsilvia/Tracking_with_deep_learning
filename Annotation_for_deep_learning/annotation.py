from typing import List
from napari import Viewer
from dask_image.imread import imread
import napari
from magicgui.widgets import ComboBox, Container
import numpy as np
from magicgui import magicgui
from napari.types import ImageData
import glob
import pandas as pd
import RearrangeData 
import pathlib
from tkinter import filedialog
import tkinter as tk
import ObjectDetection
from skimage.io import imread
from dask import delayed
import dask.array as da
import Two_object_detection as two
import AugmentationFunctions
import os
import ToInsertVisibilityInAnnotation as TIVIA
from tkinter import messagebox
from natsort import natsorted
from auxiliary import load_labels_files
from qtpy.QtWidgets import QFileDialog
import yaml
import imageio.v3 as iio

COLOR_CYCLE = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf',
    '#feb24c',
    '#9C661f',
    '#a52a2a',
    '#ffeda0',
    '#543005',
    '#000000',
    '#fdbf6f',
    '#ffffff',
    '#e6550d',
    '#addd8e',
    '#9ebcda'
    
]





# COLOR_CYCLE = [
#     '#1f77b4',
#     '#ff7f0e',
#     '#2ca02c'

def hex_to_rgba01(hx: str):
     hx = hx.lstrip('#')
     if len(hx) in (3,4): hx = ''.join(c*2 for c in hx)  # expand short forms
     if len(hx) == 6: hx += 'FF'
     r = int(hx[0:2],16)/255.0; g = int(hx[2:4],16)/255.0
     b = int(hx[4:6],16)/255.0; a = int(hx[6:8],16)/255.0
     return (r,g,b,a)


def create_label_menu(points_layer, labels):
    """Create a label menu widget that can be added to the napari viewer dock

    Parameters:
    -----------
    points_layer    napari.layers.Points
        a napari points layer
    labels : List[str]
        list of the labels for each keypoint to be annotated (e.g., the body parts to be labeled).

    Returns:
    --------
    label_menu : Container
        the magicgui Container with our dropdown menu widget
    """
    # Create the label selection menu
    label_menu = ComboBox(label='feature_label', choices=labels)
    label_widget = Container(widgets=[label_menu])
###########################
##################################


##################################################################

    def update_label_menu(event):
        """Update the label menu when the point selection changes"""
        new_label = str(points_layer.current_properties['label'][0])
        if new_label != label_menu.value:
            label_menu.value = new_label
        print('updated')
        print(new_label)
        print(points_layer.data)
      
        

    points_layer.events.current_properties.connect(update_label_menu)

    def label_changed(event):
        """Update the Points layer when the label menu selection changes"""
        selected_label = event.value
        current_properties = points_layer.current_properties
        current_properties['label'] = np.asarray([selected_label])
        points_layer.current_properties = current_properties
        print('changed')

    label_menu.changed.connect(label_changed)

    return label_widget


def point_annotator(
        im_path: str,path: str,
        labels: List[str] ):
    """Create a GUI for annotating points in a series of images.

    Parameters
    ----------
    im_path : str
        glob-like string for the images to be labeled.
    labels : List[str]
        list of the labels for each keypoint to be annotated (e.g., the body parts to be labeled).
    """
    global SHAPE_STACK
    global LABELS
    global IM_PATH
    global PATH_FOLDER
    PATH_FOLDER = path
    IM_PATH = im_path
    #function to read the images
   # PadImages_save(im_path) #pad if the images are not the same size

    stack = LoadImages(im_path)
    # LABELS = labels
    # stack = imread(im_path)
    SHAPE_STACK = stack.shape
    print(SHAPE_STACK)
   
   
    viewer = napari.view_image(stack)
    #to change the current position
    viewer.dims.current_step = (0,255,255)
   # features = {'label': np.empty(3, dtype=int)}
    properties = {'label': labels}
    # add the points
    #create a big layer and cut it for the number of labels
    #arrayModel = [[0,100,-1],[0,200,-1],[0,300,-1],[0,400,-1],[0,500,-1],[0,600,-1],[0,700,-1],[0,800,-1],[0,900,-1],[0,1000,-1],[0,1100,-1],[0,1200,-1]]
    #points= arrayModel[0:len(labels)]
   # points = np.array([[0,100,-1],[0,200,-1],[0,300,-1],[0,400,-1]])
    
    points = []
    labelsnew = labels
    labels1=[]
    arrayModel = []
    for index in range(SHAPE_STACK[0]):
        #for location in range(100,351,20):
         #   arrayModel.append([index,location,-1])
       
        arrayModel = [[index,100,-1],[index,200,-1],[index,300,-1],[index,400,-1],[index,500,-1],[index,600,-1],[index,700,-1],[index,800,-1],[index,900,-1],[index,1000,-1],[index,1100,-1],[index,1200,-1],
                     [index,100,100],[index,200,100],[index,300,100],[index,400,100],[index,500,100],[index,600,100],[index,700,100],[index,800,100],[index,900,100],[index,1000,-100],[index,1100,100],[index,1200,100]]
        points = points + arrayModel[0:len(labelsnew)]
        labels1 = labels1 + labelsnew
        # print(points)
        # print(labels)
  
   # build arrays
    points = np.asarray(points, dtype=float)             # (N, 3)
    labels_arr = np.asarray(labels1, dtype=object)       # (N,)

# safe cycle (drop any weird entries)
    SAFE_COLOR_CYCLE = [c for c in COLOR_CYCLE if c and c != '#0000']

# map each unique label -> a hex color (cycle if you have more labels than colors)
    uniq_labels = list(dict.fromkeys(labels_arr))        # preserve first-seen order
    label_to_hex = {lab: SAFE_COLOR_CYCLE[i % len(SAFE_COLOR_CYCLE)]
                for i, lab in enumerate(uniq_labels)}

    

    label_to_rgba = {lab: hex_to_rgba01(h) for lab, h in label_to_hex.items()}
    face_rgba = np.asarray([label_to_rgba[lab] for lab in labels_arr], dtype=float)  # (N,4)

# add points: pass numeric colors directly; keep 'label' for your UI
    properties = {'label': labels_arr}
    points_layer = viewer.add_points(
    points,
    properties=properties,
    face_color=face_rgba,          # numeric RGBA per point (no categorical parsing)
    edge_color=face_rgba,
    edge_width=1,
    edge_width_is_relative=True,
    symbol='o',
    size=15,
    ndim=3,
    name="keypoints",
)

# (optional) set a starting label for your menu logic
    points_layer.current_properties = {'label': np.array([uniq_labels[0]], dtype=object)}

   
        

  
  
   
#####################
# add the polygons
    polygons = []
    for index in range(SHAPE_STACK[0]):
        polygons.append(np.array([[ index,  879.52867728,  592.9339079 ],
           [   index        ,  879.52867728,  906.41696375],
           [   index        , 1260.79185332,  906.41696375],
           [   index        , 1260.79185332,  592.9339079 ]]))
    layer_shapes = viewer.add_shapes(
        polygons,
        shape_type='polygon',
        edge_width=3,
        edge_color='coral',
        face_color='#0000',
        name='boxes',
        )
    
    
    
####################################
    # add the label menu widget to the viewer
    label_widget = create_label_menu(points_layer, labels)
    viewer.window.add_dock_widget(label_widget)
    viewer.window.add_dock_widget(my_widget1,area='right')
    viewer.window.add_dock_widget(widget2,area='right')
    viewer.window.add_dock_widget(widget3,area='right')
    viewer.window.add_dock_widget(widget4,area='right')
    viewer.window.add_dock_widget(widget5,area='right')
    viewer.window.add_dock_widget(widget6, area = 'right')
    viewer.window.add_dock_widget(widget_split, area='right')
    viewer.window.add_dock_widget(widget_split_left_text, area='right')
   # viewer.window.add_dock_widget(widget_split_right_text, area='right')    
    
    napari.run()

    @viewer.bind_key('.')
    def next_label(event=None):
        """Keybinding to advance to the next label with wraparound"""
        current_properties = points_layer.current_properties
        current_label = current_properties['label'][0]
        ind = list(labels).index(current_label)
        new_ind = (ind + 1) % len(labels)
        new_label = labels[new_ind]
        current_properties['label'] = np.array([new_label])
        points_layer.current_properties = current_properties

    def next_on_click(layer, event):
        """Mouse click binding to advance the label when a point is added"""
        if layer.mode == 'add':
            next_label()

            # by default, napari selects the point that was just added
            # disable that behavior, as the highlight gets in the way
            layer.selected_data = {}

    points_layer.mode = 'add'
    points_layer.mouse_drag_callbacks.append(next_on_click)

    @viewer.bind_key(',')
    def prev_label(event):
        """Keybinding to decrement to the previous label with wraparound"""
        current_properties = points_layer.current_properties
        current_label = current_properties['label'][0]
        ind = list(labels).index(current_label)
        n_labels = len(labels)
        new_ind = ((ind - 1) + n_labels) % n_labels
        new_label = labels[new_ind]
        current_properties['label'] = np.array([new_label])
        points_layer.current_properties = current_properties
     
    @viewer.bind_key('s')
    def save_data(event=None):
         print(points_layer.data)
        

        
#Auxiliary functions
def arrange(shape,labels,points,rect,PATH_FOLDER):
    #print(shape)
    l = labels 
    p = points
    r = rect
    file = widget2()
    print(file)
    print('now')
    print(points)
   
    objectmouse = RearrangeData.HelperFunctions()
    objectmouse.GetRectangleInf(r,'mouse_0',IM_PATH,PATH_FOLDER)
    print('second')
    objectmouse.GetPointsInf(labels,points,LABELS)
    print('third')
    objectmouse.FusionData(PATH_FOLDER)
    objectmouse.ConverionPandastoText(PATH_FOLDER,shape,IM_PATH)
   
    a = 1
    
'''
output: create yaml file if it isn't exist
'''
def create_yaml_file(PATH_FOLDER, number_keypoints):
    file_path = os.path.join(PATH_FOLDER, "conf_pose.yaml")

    if not os.path.exists(file_path):
      config = {
          "path" : PATH_FOLDER,
          "train" : "images/train",
          "val"  : "images/val",
          "kpt_shape" : [number_keypoints, 3], # number of keypoints, number of dims
           # "flip_idx": [0,2,1,3,4],  # uncomment if needed
           "names": {
               0: "blind_mole"
            }
         } 
      
      with open(file_path, "w") as f:
          yaml.dump(config, f, default_flow_style=False, sort_keys=False)
          print(f"YAML file created at: {file_path}")
    else:
        print("File does not exist:", file_path)

         
@magicgui(call_button='Save Data')
def my_widget1(layer: napari.layers.Points,array:ImageData,layerShape:napari.layers.Shapes):
#def my_widget1():
       # rect = array


       
       shape = SHAPE_STACK
       labels = layer.properties
        
       points = layer.data
       rect = layerShape.data
       
       arrange(shape,labels['label'],points,rect,PATH_FOLDER)

       #create a yaml file for later use if it is not exist inside the path folder
       create_yaml_file(PATH_FOLDER, len(np.unique(labels['label'])))
      
       return 0

        
@magicgui(call_button='Save Data')
def my_widget1(layer: napari.layers.Points,array:ImageData,layerShape:napari.layers.Shapes):
#def my_widget1():
       # rect = array
       shape = SHAPE_STACK
       labels = layer.properties
        
       points = layer.data
       rect = layerShape.data
       
       arrange(shape,labels,points,rect,PATH_FOLDER)
       
       #create a yaml file for later use if it is not exist inside the path folder
       create_yaml_file(PATH_FOLDER, len(np.unique(labels['label'])))
      
       return 0

@magicgui(call_button="Load old annotations")   
def widget6(layer: napari.layers.Points,layerShape:napari.layers.Shapes):
    folder_selected = QFileDialog.getExistingDirectory(None,'Select folder with label with visibility .txt files')
    if not folder_selected:
        print("No folder selected.")
        return
    filenames = natsorted(glob.glob(IM_PATH))

    # Read all shapes
    shapes = [imread(fn).shape for fn in filenames]

    box, points, labels_all = load_labels_files(folder_selected, SHAPE_STACK[0], LABELS, SHAPE_STACK, PATH_FOLDER,shapes)
    #clear existing points
    layer.data = np.array(points)
    layerShape.data = np.array(box)
    layer.properties['label'] = np.array(labels_all)
    
    print("✅ Old annotations loaded.")  
    
   
@magicgui(path={'mode': 'd'}, call_button='Run')
def widget2(path =  pathlib.Path.home()):
    print(path)
    return (path)

# @magicgui(call_button='Augment the data')
# def widget3( ):
#     print(PATH_FOLDER)
    
@magicgui(call_button='Augment the data')
def widget3( ):
    #get file with images
    filenames = natsorted(glob.glob(IM_PATH))
    for f in filenames:
       print(f)
       object_augmentation = AugmentationFunctions.AugmentationFunctions(f,PATH_FOLDER)
       
       object_augmentation.arrangeBbox()
       object_augmentation.arrangeKeypoints()
       object_augmentation.augmentation()

    
    
@magicgui(call_button='Augment images')
def widget4( ):
    #get file with images
    filenames = natsorted(glob.glob(IM_PATH))
    for f in filenames:
       object_augmentation = AugmentationFunctions.AugmentationFunctions(f,PATH_FOLDER)
       
       #object_augmentation.arrangeBbox()
       object_augmentation.augmentationImageHorizontal()
       object_augmentation.augmentationImageVertical()

'''
Script add visibility to the annotation data in keypoints

IN dim=3 visibility values are = 0 not visible
1 is partial visible
2 is visible

Steps for the script:
    1)- Read the files from the folder
    2)- for each file read the text with  f.read
    3)- split the string into a list
    4)- insert  the number 2 after the keypoints coordinates
    if the element before is nan insert 0
    5)- convert into text

'''
@magicgui(call_button='Add visibility to the labels files')
def widget5( ):
   #change the name of a folder
   # Define the current folder name and the new folder name
   current_folder_name = PATH_FOLDER + '//labels//train'
   new_folder_name = PATH_FOLDER + '//labels//train_without_vis'
  
   # Rename the folder
   os.rename(current_folder_name, new_folder_name)
   #Create a new folder
   os.mkdir(current_folder_name)
   files = glob.glob(new_folder_name + '/*.txt')
   
   for f in files:
        object_visibility = TIVIA.AddVisibility(f,current_folder_name)
        object_visibility()

'''
add a button to split images and reorder the text information widget_split
'''
@magicgui(call_button='split images left and right')
def widget_split():
    filenames = natsorted(glob.glob(IM_PATH))
    for fn in filenames:
        img = imread(fn)
        base = os.path.basename(fn)
        split_x = get_split_position(img, base)
        left = img[:, :split_x]
        right = img[:, split_x:]
 
        iio.imwrite(os.path.join(PATH_FOLDER, f"left_{base}"), left)
        iio.imwrite(os.path.join(PATH_FOLDER, f"right_{base}"), right)

#auxiliary function
def get_split_position(img, base):
    h,w = img.shape[:2]
    
    if h==2000 and w==2000:
        split_x = 504
    else:
        split_x = 828

    return split_x
    
'''
add button to arrange left from split images
'''
@magicgui(call_button='txt file for left split images')
def widget_split_left_text():
    filenames = natsorted(glob.glob(IM_PATH))
    for fn in filenames:
        img = imread(fn)
        base = os.path.basename(fn)

        txt_path = os.path.join(PATH_FOLDER, "labels", "train", base.replace(".png", ".txt"))

        split_x = get_split_position(img, base)

        out_path = os.path.join(PATH_FOLDER, "labels", "train",f"left_{base.replace('.png','.txt')}")
        process_left_from_txt(txt_path, img, split_x, out_path)

    print("✅ LEFT labels updated from existing YOLO")


def process_left_from_txt(txt_path, img, split_x, out_path):
    h, w = img.shape[:2]

    # read
    cls, cx, cy, bw, bh, kpts = read_yolo_pose(txt_path)

    # denormalize
    cx, cy, bw, bh, keypoints = denormalize(cx, cy, bw, bh, kpts, w, h)

    # split LEFT
    cx, cy, bw, bh, keypoints = split_left_yolo(cx, cy, bw, bh, keypoints, split_x)

    # normalize
    cx, cy, bw, bh, kpts_norm = normalize_left(cx, cy, bw, bh, keypoints, split_x, h)

    # save
    save_yolo_pose(cls, cx, cy, bw, bh, kpts_norm, out_path)


def read_yolo_pose(path):
    with open(path, "r") as f:
        line = f.readline().strip().split()

    cls = int(line[0])
    cx, cy, bw, bh = map(float, line[1:5])

    kpts = list(map(float, line[5:]))

    return cls, cx, cy, bw, bh, kpts

def denormalize(cx, cy, bw, bh, kpts, w, h):
    cx *= w
    cy *= h
    bw *= w
    bh *= h

    keypoints = []
    for i in range(0, len(kpts), 3):
        x = kpts[i] * w
        y = kpts[i+1] * h
        v = kpts[i+2]
        keypoints.append([x, y, v])

    return cx, cy, bw, bh, keypoints

def split_left_yolo(cx, cy, bw, bh, keypoints, split_x):
    # bounding box corners
    x1 = cx - bw/2
    x2 = cx + bw/2

    # clip to LEFT
    x1 = max(0, x1)
    x2 = min(split_x, x2)

    new_bw = x2 - x1
    new_cx = (x1 + x2) / 2

    # filter keypoints
    new_kpts = []
    for x, y, v in keypoints:
        if x < split_x and not np.isnan(x):
            new_kpts.append([x, y, v])
        else:
            new_kpts.append([0, 0, 0])  # YOLO expects placeholder

    return new_cx, cy, new_bw, bh, new_kpts

def normalize_left(cx, cy, bw, bh, keypoints, split_x, h):
    cx /= split_x
    bw /= split_x
    cy /= h
    bh /= h

    kpts_norm = []
    for x, y, v in keypoints:
        if v == 0:
            kpts_norm.extend([0, 0, 0])
        else:
            kpts_norm.extend([x / split_x, y / h, v])

    return cx, cy, bw, bh, kpts_norm

def save_yolo_pose(cls, cx, cy, bw, bh, kpts, path):
    line = f"{cls} {cx} {cy} {bw} {bh} " + " ".join(map(str, kpts))
    with open(path, "w") as f:
        f.write(line + "\n")


# '''
# Add menu for object detection
# '''

# @magicgui(call_button='Save Data')
# def my_widget_shape(array:ImageData,layerShape:napari.layers.Shapes):
# #def my_widget1():
#        # rect = array
       
    
#        rect = layerShape.data
      
#        print(rect)
       
       
#       # arrange(shape,labels,points,rect,PATH_FOLDER)
      
#        return 0

#Load the pictures as a stack
def PadImages_save(im_path):
    filenames = natsorted(glob.glob(im_path))

    # Read all shapes
    shapes = [imread(fn).shape for fn in filenames]
     # 🔹 Check if all shapes are identical
    if len(set(shapes)) == 1:
        print("All images already have the same shape. Skipping padding.")
        return

    max_y = max(s[0] for s in shapes)
    max_x = max(s[1] for s in shapes)
    target_shape = (max_y, max_x)

    #padding
    for fn in filenames:
        img = imread(fn)
        pad_y = target_shape[0] - img.shape[0]
        pad_x = target_shape[1] - img.shape[1]
        padded = np.pad(img, ((0, pad_y), (0, pad_x), (0, 0)), mode='constant')
   
        # decide where to save-rewrite the file
        out_path = fn
        iio.imwrite(out_path, padded)

#Load the pictures as a stack
def LoadImages(im_path):
    filenames = natsorted(glob.glob(im_path))
   # read the first file to get the shape and dtype
   # ASSUMES THAT ALL FILES SHARE THE SAME SHAPE/TYPE
    sample = imread(filenames[0])

    lazy_imread = delayed(imread)  # lazy reader
    lazy_arrays = [lazy_imread(fn) for fn in filenames]
    dask_arrays = [
    da.from_delayed(delayed_reader, shape=sample.shape, dtype=sample.dtype)
    for delayed_reader in lazy_arrays
    ]
# Stack into one large dask.array
    stack = da.stack(dask_arrays, axis=0)
    
    return stack



'''
Create a selection list
'''
def CreateListBox():
   
   app = tk.Tk()
   app.title('List box')

   
   
   def clicked():
    global LABELS
    print("clicked")
    LABELS =[]
    
    selected = box.curselection()  # returns a tuple
    for idx in selected:
        aux= box.get(idx)
        LABELS.append(aux)
        
    print(LABELS)
    

   box = tk.Listbox(app, selectmode=tk.MULTIPLE, height=10)
   #ARRANGE TO HAVE MICE AND BLIND MOLE
   if SELECTION_Animal[0] == "Mice":
      values = ['nose','ear_Left', 'ear_Right', 'shoulders', 'center', 'hips_left','hips_right', 'tail_Base', 'tail_round', 'tail_2', 'tail_End']
   # values = ['BM_snout', 'BM_lower_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom', 
   #            'BM_head','BM_centroid', 'BM_back', 'BM_right_rear_leg_1', 'BM_right_rear_leg_2', 
   #            'BM_left_rear_leg_1', 'BM_left_rear_leg_2','BM_right_front_leg_1','BM_right_front_leg_2','BM_left_front_leg_1',
   #            'BM_left_front_leg_2','BM_above_snout','BM_Below_snout','BM_below_mouth', 
   #            'BM_behind','BM_above_behind','BM_below_behind', 'BM_low_behind']
   elif  SELECTION_Animal[0] == 'Blind moles from the side':
   # VALUES OF SIDE:
       values = ['BM_snout', 'BM_lower_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom', 
             'BM_head','BM_centroid', 'BM_back', 'BM_right_rear_leg_1', 'BM_left_rear_leg_1',
              'BM_right_front_leg_1','BM_left_front_leg_1','BM_behind', 'BM_low_behind', 'BM_below_mouth', 'BMR_Middle']
       
   elif SELECTION_Animal[0] == 'Blind moles from the top':
   
   # VALUES OF UP:
       values =  ['BM_right_snout', 'BM_center_snout', 'BM_left_snout' , 'BM_mouth', 'BM_right_ridge', 'BM_left_ridge', 'BM_right_ear', 'BM_left_ear', 'BM_left_forelimb', 'BM_right_forelimb', 'BM_left_hindlimb', 'BM_right_hindlimb', 'BM_pelvic_base', 'BM_right_side', 'BM_left_side', 'BM_centr', 'BM_left_hip', 'BM_right_hip' ]
   #values =  ['BM_snout', 'BM_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom', 'BM_head_right','BM_head_left', 'BM_right_front_leg', 'BM_left_front_leg','BM_right_rear_leg','BM_left_rear_leg','BM_behind', 'BM_right_back', 'BM_left_back', 'BM_centroid_left', 'BM_centroid_right']
   
   
   
   
   for val in values:
    box.insert(tk.END, val)
   box.pack()

   button = tk.Button(app, text='ADD labels', width=25, command=clicked)
   button.pack()

   exit_button = tk.Button(app, text='Close', width=25, command=app.destroy)
   exit_button.pack()

   app.mainloop()

     
'''
Create a selection list object detection or pose detection
'''
def SelectListBox():
   
   app = tk.Tk()
   app.title('List box')

   
   
   def clicked():
    global SELECTION
    print("clicked")
    SELECTION =[]
    
    selected = box.curselection()  # returns a tuple
    for idx in selected:
        aux= box.get(idx)
        SELECTION.append(aux)
        
    print(SELECTION)
    

   box = tk.Listbox(app, selectmode=tk.MULTIPLE, height=10)
   values = ['Two no similar objects detection','Pose detection','Two similar object detection']
   #values = ['Two object detection','Pose detection','Pose detection 2 objects']
   for val in values:
    box.insert(tk.END, val)
   box.pack()

   button = tk.Button(app, text='ADD labels', width=25, command=clicked)
   button.pack()

   exit_button = tk.Button(app, text='Close', width=25, command=app.destroy)
   exit_button.pack()

   app.mainloop()
   
def SelectListBoxAnimal():
 app = tk.Tk()
 app.title('List box')

 
 
 def clicked():
  global SELECTION_Animal
  print("clicked")
  SELECTION_Animal =[]
  
  selected = box.curselection()  # returns a tuple
  for idx in selected:
      aux= box.get(idx)
      SELECTION_Animal.append(aux)
      
  print(SELECTION_Animal)
  

 box = tk.Listbox(app, selectmode=tk.MULTIPLE, height=10,width = 30)
 values = ['Mice','Blind moles from the side','Blind moles from the top']
 #values = ['Two object detection','Pose detection','Pose detection 2 objects']
 for val in values:
  box.insert(tk.END, val)
 box.pack()

 button = tk.Button(app, text='ADD animals', width=25, command=clicked)
 button.pack()

 exit_button = tk.Button(app, text='Close', width=25, command=app.destroy)
 exit_button.pack()

 app.mainloop()


def main():
    global PATH_FOLDER
    
    SHAPE_STACK = ()
    #PATH_FOLDER = 'F://PoseYolo//train'
    #show message
    messagebox.showinfo("Note", "Create a folder with 2 subfolders called:\n images,labels\n create 2 other subfolders inside each one of these 2 folders:\n called: train and val ")
    PATH_FOLDER = filedialog.askdirectory(title = 'Enter the directory which includes 2 folders,images and labels \n (note: labels folder is empty)')
    
    im_path = PATH_FOLDER + '//images//train//*.png'
   
    filenames = natsorted(glob.glob(im_path))
    
    print(filenames)

   #Create a list which select the animal
    
    #Create a selection list
    SelectListBox()
    print(SELECTION)
    if SELECTION[0] == 'Pose detection':
       print('ok')
       #Create a list which select the animal
       SelectListBoxAnimal()
       #add the selection of points according to animal
       CreateListBox()

       point_annotator(im_path,PATH_FOLDER, labels = LABELS)
    # elif SELECTION[0] == 'Pose detection 2 objects':
    #    print('ok')
    #    CreateListBox()
    #    viewer = two.create_viewer(im_path,PATH_FOLDER)
    #    two.point_annotator(viewer,  'points_mouse0', 'coral', 'shape_mouse0',labels = LABELS)
    #    two.point_annotator(viewer, 'points_mouse1', 'blue', 'shape_mouse1',labels = LABELS)
       
    elif SELECTION[0] == 'Two no similar objects detection':
        SameObj = False
        
        ObjectDetection.box_annotator(im_path,PATH_FOLDER, SameObj)
    else:
        SameObj= True
        ObjectDetection.box_annotator(im_path,PATH_FOLDER, SameObj)
        
    
    

    

if __name__ == "__main__":
    main()