@echo off
rem // Prompt the user for input
set /p UserInput="Please enter the link to the stream for the script: "

rem // Define the path to your Conda installation's Scripts folder
rem set "CONDA_SCRIPTS=C:\ProgramData\Miniconda3\Scripts"
rem // Alternatively, for a user install or Anaconda:
rem set "CONDA_SCRIPTS=C:\Users\Username\anaconda3\Scripts"

rem // Define the name of your environment
set "CONDA_ENV=auto-editor"

rem // Activate the environment by directly calling the script
call "%CONDA_SCRIPTS%\activate.bat" %CONDA_ENV%

rem // Run your Python script with the user input
python "src\main.py" "%UserInput%"

rem // Deactivate
call "%CONDA_SCRIPTS%\deactivate.bat"

pause