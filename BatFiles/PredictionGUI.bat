@echo off

set conda_environment=Yolo_detection
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "C:\LabSoftware\Tracking_with_deep_learning\Objectdetection2mice\Main.py" 
call %conda_path%\Scripts\deactivate