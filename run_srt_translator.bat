@echo off
echo SRT Translator Application
echo =========================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show googletrans >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements_srt_translator.txt
    if errorlevel 1 (
        echo Error: Failed to install required packages
        pause
        exit /b 1
    )
)

echo.
echo Starting SRT translation...
echo.

REM Run the translator
python srt_translator.py

echo.
echo Translation completed!
pause
