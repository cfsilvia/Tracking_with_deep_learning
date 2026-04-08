import yaml
"""create yaml for the object2mice detections
    """

# Define the settings with several branches
TwoObjectDetection_settings= {
  'type_experiment' : 'Blind moles from the side',
  'file_model' : ['D:/Silvia/Blindmole_deep_learning/models/yoloBMR_left_BMR_combined_videos_07.07.242/weights/best.pt',
                  'D:/Silvia/Blindmole_deep_learning/models/yoloBMR_right_BMR_combined_videos_26.06.242/weights/best.pt'],
    'video_path' : 'D:/Silvia/Blindmole_deep_learning/BMR2_cfosExp_exp1_27.10.21_side.avi',
    'video_output' : 'D:/Silvia/Blindmole_deep_learning/output/BMR2_with_landmarks.avi',
    'x_crop' : 0.5  # divider for left/right separation, fraction of frame width
}

# Write the settings to a YAML file
with open('TwoObjectDetection.yaml', 'w') as file:
    yaml.dump(TwoObjectDetection_settings, file, default_flow_style=False)