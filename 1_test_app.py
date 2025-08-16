#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the Audio to SRT Subtitle Generator
"""

import os
from pathlib import Path

def test_environment():
    """Test if the environment is properly set up."""
    print("Testing Audio to SRT Subtitle Generator Environment")
    print("=" * 50)
    
    # Check if media folder exists and contains MP3 files
    media_folder = Path("media")
    if media_folder.exists():
        mp3_files = list(media_folder.glob("*.mp3"))
        print(f"✓ Media folder found with {len(mp3_files)} MP3 file(s)")
        for mp3_file in mp3_files:
            print(f"  - {mp3_file.name}")
    else:
        print("✗ Media folder not found")
        return False
    
    # Check if srt_spanish folder exists
    srt_folder = Path("srt_spanish")
    if srt_folder.exists():
        srt_files = list(srt_folder.glob("*.srt"))
        print(f"✓ SRT output folder found with {len(srt_files)} SRT file(s)")
        for srt_file in srt_files:
            print(f"  - {srt_file.name}")
    else:
        print("✗ SRT output folder not found")
    
    # Check if required Python files exist
    required_files = [
        "transcript_to_srt.py",
        "simple_transcript.py",
        "requirements.txt",
        "requirements_whisper.txt",
        "README.md"
    ]
    
    print("\nChecking required files:")
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file}")
    
    # Check Python packages
    print("\nChecking Python packages:")
    try:
        import whisper
        print("  ✓ openai-whisper")
    except ImportError:
        print("  ✗ openai-whisper (install with: pip install openai-whisper)")
    
    try:
        import speech_recognition
        print("  ✓ SpeechRecognition")
    except ImportError:
        print("  ✗ SpeechRecognition (install with: pip install SpeechRecognition)")
    
    try:
        from pydub import AudioSegment
        print("  ✓ pydub")
    except ImportError:
        print("  ✗ pydub (install with: pip install pydub)")
    
    print("\n" + "=" * 50)
    print("Environment test completed!")
    
    return True

if __name__ == "__main__":
    test_environment()
