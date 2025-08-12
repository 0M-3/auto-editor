@echo off
setlocal enabledelayedexpansion

:: Define the name of the file containing the URLs
set "url_file=url.txt"

:: Check if the url file exists
if not exist "%url_file%" (
    echo Error: "%url_file%" not found.
    goto :eof
)

:: Loop through each line in the url file
for /f "delims=" %%a in ('type "%url_file%"') do (
    :: Trim leading/trailing whitespace from the URL
    set "current_url=%%a"
    for /f "tokens=*" %%b in ("!current_url!") do set "trimmed_url=%%b"

    :: Skip empty lines
    if not "!trimmed_url!"=="" (
        echo Running python main.py with URL: !trimmed_url!
        :: Execute the python script with the current URL as an argument
        python src/main.py "!trimmed_url!"
        :: You can add error handling here if needed, e.g.,
        :: if %errorlevel% neq 0 (
        ::     echo Error running script for URL: !trimmed_url!
        :: )
    )
)

echo Script finished.
pause
