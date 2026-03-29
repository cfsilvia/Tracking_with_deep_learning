# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 15:01:28 2024

@author: Administrator
"""
from auxiliary_functions import auxiliary_functions
import cv2
from Frame_treatment import CreatePlot
#Use Agg backend for canvas

# =============================================================================
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd 
import os



class Manager_data:
    
   def Manager_data( middle_tube_y, middle_tube_x, input_excel, input_video, sheet_name, column_name, _outputVideo,_upper_tube, _lower_tube, _fps,_if_Cropped,
                    _if_Plot_left,input_excel_left = 0, title = 0,xstart = 0, ystart = 0, xend = 0, yend = 0):
       if  _if_Plot_left == 0:
       #-1- Get data to plot 
            data_to_plot = auxiliary_functions.read_excel( middle_tube_y, middle_tube_x, input_excel, sheet_name, column_name,_upper_tube, _lower_tube)
        #-2- Save data to plot 
            data_to_save = data_to_plot
            Manager_data.SaveData(data_to_save, input_excel, column_name)
        
        #-3- Create new movie from the video
            up_line = middle_tube_y - _upper_tube
            down_line = -_lower_tube  +  middle_tube_y

        #if the data is normalized  with zscore
            data_to_plot = (data_to_plot - data_to_plot.mean()) / data_to_plot.std()  
            Manager_data.Create_new_movie(input_video, data_to_plot,_outputVideo,_fps, up_line, down_line,_if_Cropped)
            
       else:
        #-1- Get data to plot 
            data_to_plot = auxiliary_functions.read_excel( middle_tube_y, middle_tube_x, input_excel, sheet_name, column_name,_upper_tube, _lower_tube)
            data_to_plot_left = auxiliary_functions.read_excel( middle_tube_y, middle_tube_x, input_excel_left, sheet_name, column_name,_upper_tube, _lower_tube)
        #-3- Save data to plot 
            data_to_save = pd.DataFrame({'Left_side':data_to_plot, 'Right_side':data_to_plot_left})
            Manager_data.SaveData(data_to_save, input_excel, column_name)
        #-2- Create new movie from the video
            up_line = middle_tube_y - _upper_tube
            down_line = -_lower_tube  +  middle_tube_y
            Manager_data.Create_new_movie(input_video, data_to_plot,_outputVideo,_fps, up_line, down_line,_if_Cropped,data_to_plot_left, title,
                                          xstart, ystart, xend, yend)
             
   def Create_new_movie(input_video, data_to_plot,_outputVideo,_fps,up_line, down_line, _if_Cropped,data_to_plot_left = None,title = None,
                        xstart = 0, ystart = 0, xend = 0, yend = 0):
    matplotlib.pyplot. ioff()
    #counter
    counter_frame = 0
    # Create a VideoCapture object
    cap = cv2.VideoCapture(input_video)
    
    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()
    
    # Get the frames per second (fps)
    _fps = cap.get(cv2.CAP_PROP_FPS)
    #_fps =24.004
    
    # Read the video frame by frame
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
    
        # If frame is read correctly ret is True
        if not ret:
            print("Reached end of video or failed to read frame.")
            break
        #%%
        #crop the image
        # Define the ROI (top-left corner and bottom-right corner)
        x_start, y_start = xstart, ystart# 0, 730  # Top-left corner
        x_end, y_end = xend, yend #2000, 2000    # Bottom-right corner
        
        if _if_Cropped == 1:
           cropped_image = frame[y_start:y_end, x_start:x_end]
           frame = cropped_image 
        #Create a plot with the frame and the data
        #Create an instance inside a 
        instance1 =CreatePlot(frame, data_to_plot, counter_frame,up_line, down_line,data_to_plot_left,title)
        instance1.SelectDataToPlot()
        img,fig = instance1.FillSubplot()
        #%% Save image
        if counter_frame == 0:
           height = img.shape[0]
           width = img.shape[1] 
           writer = cv2.VideoWriter(_outputVideo ,cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), _fps, (width,height))
          # writer = cv2.VideoWriter(_outputVideo ,cv2.VideoWriter_fourcc('M','J','P','G'), _fps, (width,height))
        writer.write(img)
        
        
        #%%
        # Display the resulting frame
       # cv2.imshow('Frame', img)
    
        # Press 'q' to exit the video before it ends
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        plt.close(fig)
        print(counter_frame)
        counter_frame += 1
    # Release the video capture object
    cap.release()
     
      
# When everything done, release the video capture object
   
  # writer.release()

 # Closes all the frames
   cv2.destroyAllWindows()
   
   '''
   Save data
   '''
   def SaveData(data_to_save, input_excel,column_name):
       #get path 
       directory = os.path.dirname(input_excel)
       #get file name
       file_name_without_extension = os.path.splitext(os.path.basename(input_excel))[0]
       # save data into excel file
       output = directory + '/' + file_name_without_extension + '_ToPlot' + '.xlsx'
       with pd.ExcelWriter(output) as writer:
            data_to_save.to_excel(writer, sheet_name = column_name, index=False)