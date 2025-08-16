#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio to SRT Subtitle Generator
Transcribes MP3 audio files to SRT subtitle format for Spanish (Latin American) content.
"""

import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pysrt
import re
import sys
from pathlib import Path

class AudioToSRTConverter:
    def __init__(self, media_folder="media", output_folder="srt_spanish"):
        """
        Initialize the converter with input and output folders.
        
        Args:
            media_folder (str): Path to folder containing MP3 files
            output_folder (str): Path to folder where SRT files will be saved
        """
        self.media_folder = Path(media_folder)
        self.output_folder = Path(output_folder)
        self.recognizer = sr.Recognizer()
        
        # Create output folder if it doesn't exist
        self.output_folder.mkdir(exist_ok=True)
        
        # Configure recognizer for better Spanish recognition
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
    def convert_mp3_to_wav(self, mp3_path):
        """
        Convert MP3 file to WAV format for better speech recognition.
        
        Args:
            mp3_path (Path): Path to MP3 file
            
        Returns:
            Path: Path to temporary WAV file
        """
        try:
            print(f"Converting {mp3_path.name} to WAV format...")
            audio = AudioSegment.from_mp3(mp3_path)
            
            # Export as WAV
            wav_path = mp3_path.with_suffix('.wav')
            audio.export(wav_path, format="wav")
            print(f"Conversion completed: {wav_path.name}")
            return wav_path
            
        except Exception as e:
            print(f"Error converting MP3 to WAV: {e}")
            return None
    
    def split_audio_on_silence(self, audio_path, min_silence_len=500, silence_thresh=-40):
        """
        Split audio into chunks based on silence detection.
        
        Args:
            audio_path (Path): Path to audio file
            min_silence_len (int): Minimum silence length in milliseconds
            silence_thresh (int): Silence threshold in dB
            
        Returns:
            list: List of audio chunks
        """
        try:
            print("Splitting audio into chunks based on silence...")
            audio = AudioSegment.from_wav(audio_path)
            
            # Split audio on silence
            chunks = split_on_silence(
                audio,
                min_silence_len=min_silence_len,
                silence_thresh=silence_thresh,
                keep_silence=100  # Keep 100ms of silence for natural breaks
            )
            
            print(f"Audio split into {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            print(f"Error splitting audio: {e}")
            return []
    
    def transcribe_chunk(self, chunk, chunk_index, chunk_duration):
        """
        Transcribe a single audio chunk.
        
        Args:
            chunk: AudioSegment chunk
            chunk_index (int): Index of the chunk
            chunk_duration (int): Duration of the chunk in milliseconds
            
        Returns:
            dict: Dictionary with transcription text and timing info
        """
        try:
            # Export chunk to temporary WAV file
            temp_wav = f"temp_chunk_{chunk_index}.wav"
            chunk.export(temp_wav, format="wav")
            
            # Recognize speech
            with sr.AudioFile(temp_wav) as source:
                audio_data = self.recognizer.record(source)
                
                # Use Google Speech Recognition with Spanish language
                text = self.recognizer.recognize_google(
                    audio_data, 
                    language="es-419"  # Spanish (Latin American)
                )
                
                # Clean up temporary file
                os.remove(temp_wav)
                
                return {
                    'text': text,
                    'start_time': chunk_index * chunk_duration,
                    'end_time': (chunk_index + 1) * chunk_duration
                }
                
        except sr.UnknownValueError:
            print(f"Chunk {chunk_index}: Speech not recognized")
            os.remove(temp_wav) if os.path.exists(temp_wav) else None
            return None
        except sr.RequestError as e:
            print(f"Chunk {chunk_index}: Could not request results; {e}")
            os.remove(temp_wav) if os.path.exists(temp_wav) else None
            return None
        except Exception as e:
            print(f"Chunk {chunk_index}: Error during transcription: {e}")
            os.remove(temp_wav) if os.path.exists(temp_wav) else None
            return None
    
    def format_time(self, milliseconds):
        """
        Convert milliseconds to SRT time format (HH:MM:SS,mmm).
        
        Args:
            milliseconds (int): Time in milliseconds
            
        Returns:
            str: Formatted time string
        """
        seconds = milliseconds // 1000
        milliseconds = milliseconds % 1000
        
        hours = seconds // 3600
        seconds = seconds % 3600
        minutes = seconds // 60
        seconds = seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def create_srt_content(self, transcriptions):
        """
        Create SRT content from transcriptions.
        
        Args:
            transcriptions (list): List of transcription dictionaries
            
        Returns:
            str: SRT formatted content
        """
        srt_content = ""
        
        for i, trans in enumerate(transcriptions, 1):
            if trans and trans['text'].strip():
                start_time = self.format_time(trans['start_time'])
                end_time = self.format_time(trans['end_time'])
                
                # Clean and format text
                text = trans['text'].strip()
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
            
            # Convert MP3 to WAV
            wav_path = self.convert_mp3_to_wav(mp3_path)
            if not wav_path:
                return False
            
            # Split audio into chunks
            chunks = self.split_audio_on_silence(wav_path)
            if not chunks:
                print("No audio chunks found")
                return False
            
            # Calculate chunk duration
            total_duration = sum(len(chunk) for chunk in chunks)
            chunk_duration = total_duration // len(chunks)
            
            print("Transcribing audio chunks...")
            transcriptions = []
            
            for i, chunk in enumerate(chunks):
                print(f"Processing chunk {i+1}/{len(chunks)}...")
                transcription = self.transcribe_chunk(chunk, i, chunk_duration)
                transcriptions.append(transcription)
            
            # Create SRT content
            srt_content = self.create_srt_content(transcriptions)
            
            # Save SRT file
            srt_filename = mp3_path.stem + ".srt"
            srt_path = self.output_folder / srt_filename
            
            with open(srt_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"SRT file created: {srt_path}")
            
            # Clean up temporary WAV file
            if wav_path.exists():
                wav_path.unlink()
            
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
    """Main function to run the audio to SRT converter."""
    print("Audio to SRT Subtitle Generator")
    print("=" * 40)
    
    # Check if media folder exists
    if not Path("media").exists():
        print("Error: 'media' folder not found. Please create it and add MP3 files.")
        return
    
    # Initialize converter
    converter = AudioToSRTConverter()
    
    # Process all files
    converter.process_all_files()
    
    print("\n" + "=" * 40)
    print("Process completed. Check the 'srt_spanish' folder for generated SRT files.")

if __name__ == "__main__":
    main()
