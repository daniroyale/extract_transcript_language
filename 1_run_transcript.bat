@echo off
echo Audio to SRT Subtitle Generator
echo ================================
echo.
echo Choose your transcription method:
echo 1. Google Speech Recognition (requires internet)
echo 2. Whisper (offline, better quality)
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Running Google Speech Recognition version...
    python transcript_to_srt.py
) else if "%choice%"=="2" (
    echo.
    echo Running Whisper version...
    python simple_transcript.py
) else (
    echo Invalid choice. Please run the script again.
    pause
    exit /b 1
)

echo.
echo Press any key to exit...
pause >nul
