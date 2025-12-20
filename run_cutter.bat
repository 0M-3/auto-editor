@echo off
setlocal enabledelayedexpansion

REM ================= CONFIGURATION =================
set "TARGET_DIR=timestamps"
rem // Define the path to your Conda installation's Scripts folder
rem set "CONDA_SCRIPTS=C:\ProgramData\Miniconda3\Scripts"
rem // Alternatively, for a user install or Anaconda:
set "CONDA_SCRIPTS=C:\Users\Omkar2\anaconda3\Scripts"

rem // Define the name of your environment
set "CONDA_ENV=auto-editor"
REM =================================================

REM Check if target directory exists
if not exist "%TARGET_DIR%" (
    echo [ERROR] Folder "%TARGET_DIR%" not found.
    pause
    exit /b
)

echo Scanning "%TARGET_DIR%" for CSV files...
echo.

set count=0

REM Loop through all .csv files in the target directory
for %%f in ("%TARGET_DIR%\*.csv") do (
    set /a count+=1
    set "file[!count!]=%%~nxf"
    echo [!count!] %%~nxf
)

REM Check if files were found
if %count%==0 (
    echo No CSV files found in "%TARGET_DIR%".
    pause
    exit /b
)

echo.
set /p "selection=Select a file number (1-%count%): "

REM Validate selection
if defined file[%selection%] (
    set "selectedFile=!file[%selection%]!"
    set "videoName=!selectedFile:~0,-4!"
    echo.
    echo ------------------------------------------------
    echo Selected: !videoName!
    echo Running:  python "src\cut_together.py" !videoName!
    echo ------------------------------------------------
    echo.
    
    rem // Activate the environment by directly calling the script
    call "!CONDA_SCRIPTS!\activate.bat" %CONDA_ENV%
    REM Execute the Python script with the filename as the argument
    REM We use quotes "" around the filename in case it has spaces
    python "src\cut_together.py" !videoName!
    
    echo.
    echo Script finished.
    pause

) else (
    echo.
    echo [ERROR] Invalid selection number.
    pause
)