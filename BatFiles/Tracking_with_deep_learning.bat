
@echo off
::call activate [base]
:: cmd/k prevent to close bat file
python "C:\LabSoftware\Tracking_with_deep_learning\MainGui\MainGui\Initial.py" > output.txt


timeout /t 5 /nobreak >nul

:: Read content of output.txt into a variable using for /f
for /f "delims=" %%a in (output.txt) do set "pythonOutput=%%a"

:: Display Python script output
echo Python script output: %pythonOutput%

:: Check if pythonOutput is equal to 3
if "%pythonOutput%" equ "1" (
    echo Running another Python script...
    call AnnotationGUI.bat
	)else if "%pythonOutput%" equ "2"  (
	    echo Running another Python script...
        call TrainingGUI.bat
	)else if "%pythonOutput%" equ "3"  (
	    echo Running Prediction script...
        call PredictionGUI.bat
       	
	)else if "%pythonOutput%" equ "4"  (
	    echo Running combination data plus video script...
        call MoviePlusPredictionGUI.bat	
 			
) else (
    echo pythonOutput is not 1  3 4 5 6 7 8 9. No need to run another script.
)



:: Check if pythonOutput is 3
   
pause
:: call  