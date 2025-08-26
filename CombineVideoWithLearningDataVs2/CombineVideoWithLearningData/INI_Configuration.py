# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 14:30:24 2024

@author: Administrator
"""

# Import module
import configparser
def INI_Configuration(movie_path,video_output,excel_left, excel_right,video_final,file):
   # Create a configparser object
   config_object = configparser.ConfigParser()
   # Add sections to the configuration object
   config_object.add_section("Input_files")
   #config_object.set('Input_files', '; comment here')
   config_object.add_section("data_to_plot")
   config_object.add_section("output_file")
   config_object.add_section("settings")
   # Add field names to the configuration object for each section
   config_object.set("Input_files","excel file left mouse",excel_left)
   config_object.set("Input_files","excel file right mouse",excel_right)
   config_object.set("Input_files","input_video",video_output)
   config_object.set("Input_files","original_video",movie_path)
   config_object.set("Input_files","sheet_name",'BMR')

   config_object.set("data_to_plot","name of the column to plot","BM_snout_y")

   config_object.set("output_file","video_output",video_final)

   config_object.set("settings","middle_tube_y","1244")
   config_object.set("settings","middle_tube_x","555")
   config_object.set("settings","_upper_tube","1178")
   config_object.set("settings","_upper_tube","1310")
   config_object.set("settings","_fps","60")
   config_object.set("settings","_if_Cropped","0")
   config_object.set("settings"," _if_Plot_left","1")
   config_object.set("settings"," _title","''")
   config_object.set("settings"," _xstart","0")
   config_object.set("settings"," _ystart","730")
   config_object.set("settings"," _xend","2448")
   config_object.set("settings"," _yend","2048")

   # Save the configuration file
   with open(file,"w") as file_object:
    config_object.write(file_object)