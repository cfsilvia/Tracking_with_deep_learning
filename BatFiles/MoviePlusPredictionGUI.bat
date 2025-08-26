@echo off

set conda_environment=general_software2
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "C:\LabSoftware\Tracking_with_deep_learning\CombineVideoWithLearningDataVs2\CombineVideoWithLearningData\Initial.py" 
call %conda_path%\Scripts\deactivate