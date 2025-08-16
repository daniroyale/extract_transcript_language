#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Audio to SRT Subtitle Generator using OpenAI Whisper
Transcribes MP3 audio files to SRT subtitle format for Spanish (Latin American) content.
  pip install openai-whisper
  python simple_transcript.py
"""

import os
import whisper
import re
from pathlib import Path
from datetime import timedelta

class SimpleAudioToSRTConverter:
    def __init__(self, media_folder="media", output_folder="srt_spanish"):
        """
        Initialize the converter with input and output folders.
        
        Args:
            media_folder (str): Path to folder containing MP3 files
            output_folder (str): Path to folder where SRT files will be saved
        """
        self.media_folder = Path(media_folder)
        self.output_folder = Path(output_folder)
        
        # Create output folder if it doesn't exist
        self.output_folder.mkdir(exist_ok=True)
        
        print("Loading Whisper model...")
        # Load Whisper model (will download on first run)
        self.model = whisper.load_model("base")
        print("Whisper model loaded successfully!")
    
    def format_time(self, seconds):
        """
        Convert seconds to SRT time format (HH:MM:SS,mmm).
        
        Args:
            seconds (float): Time in seconds
            
        Returns:
            str: Formatted time string
        """
        td = timedelta(seconds=seconds)
        hours = int(td.total_seconds() // 3600)
        minutes = int((td.total_seconds() % 3600) // 60)
        seconds = td.total_seconds() % 60
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def create_srt_content(self, segments):
        """
        Create SRT content from Whisper segments.
        
        Args:
            segments (list): List of Whisper segments
            
        Returns:
            str: SRT formatted content
        """
        srt_content = ""
        
        for i, segment in enumerate(segments, 1):
            start_time = self.format_time(segment['start'])
            end_time = self.format_time(segment['end'])
            
            # Clean and format text
            text = segment['text'].strip()
            text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
            
            srt_content += f"{i}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{text}\n\n"
        
        return srt_content
    
    def process_audio_file(self, mp3_path):
        """
        Process a single MP3 file and generate SRT subtitle file.
        
        Args:
            mp3_path (Path): Path to MP3 file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"\nProcessing: {mp3_path.name}")
            
            # Transcribe audio using Whisper
            print("Transcribing audio with Whisper...")
            result = self.model.transcribe(
                str(mp3_path),
                language="es",  # Spanish
                task="transcribe"
            )
            
            # Create SRT content from segments
            segments = result['segments']
            srt_content = self.create_srt_content(segments)
            
            # Save SRT file
            srt_filename = mp3_path.stem + ".srt"
            srt_path = self.output_folder / srt_filename
            
            with open(srt_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"SRT file created: {srt_path}")
            print(f"Transcription completed with {len(segments)} segments")
            
            return True
            
        except Exception as e:
            print(f"Error processing {mp3_path.name}: {e}")
            return False
    
    def process_all_files(self):
        """
        Process all MP3 files in the media folder.
        """
        mp3_files = list(self.media_folder.glob("*.mp3"))
        
        if not mp3_files:
            print(f"No MP3 files found in {self.media_folder}")
            return
        
        print(f"Found {len(mp3_files)} MP3 file(s) to process")
        
        successful = 0
        for mp3_file in mp3_files:
            if self.process_audio_file(mp3_file):
                successful += 1
        
        print(f"\nProcessing complete: {successful}/{len(mp3_files)} files processed successfully")

def main():
    """Main function to run the simple audio to SRT converter."""
    print("Simple Audio to SRT Subtitle Generator using Whisper")
    print("=" * 55)
    
    # Check if media folder exists
    if not Path("media").exists():
        print("Error: 'media' folder not found. Please create it and add MP3 files.")
        return
    
    # Initialize converter
    converter = SimpleAudioToSRTConverter()
    
    # Process all files
    converter.process_all_files()
    
    print("\n" + "=" * 55)
    print("Process completed. Check the 'srt_spanish' folder for generated SRT files.")

if __name__ == "__main__":
    main()
