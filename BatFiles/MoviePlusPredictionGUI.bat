@echo off

set conda_environment=GeneralSoftwares
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "C:\LabSoftware\Tracking_with_deep_learning\CombineVideoWithLearningDataVs2\CombineVideoWithLearningData\Initial.py" 
call %conda_path%\Scripts\deactivate