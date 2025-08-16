# Audio to SRT Subtitle Generator

This Python application converts MP3 audio files to SRT subtitle format, specifically designed for Spanish (Latin American) content.

## Features

- Transcribes Spanish audio to text using speech recognition
- Generates properly formatted SRT subtitle files
- Splits audio into chunks based on silence detection
- Supports multiple MP3 files in batch processing
- Outputs SRT files to the `srt_spanish` folder

## Requirements

- Python 3.7 or higher
- Internet connection (for Google Speech Recognition API)
- FFmpeg (for audio processing)

## Installation

1. Install the required Python packages:
```bash
pip install -r requirements.txt
```

2. Install FFmpeg:
   - **Windows**: Download from https://ffmpeg.org/download.html or use chocolatey: `choco install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

## Usage

1. Place your MP3 audio files in the `media` folder
2. Run the application:
```bash
python transcript_to_srt.py
```

3. The generated SRT subtitle files will be saved in the `srt_spanish` folder

## Alternative: Simple Version with Whisper

For better transcription quality and easier setup, you can use the Whisper-based version:

1. Install Whisper:
```bash
pip install openai-whisper
```

2. Run the simple version:
```bash
python simple_transcript.py
```

## File Structure

```
transcript_language/
├── media/                    # Input MP3 files
├── srt_spanish/             # Generated SRT subtitle files
├── transcript_to_srt.py     # Main application
├── simple_transcript.py     # Whisper-based alternative
├── requirements.txt          # Python dependencies
└── README.md               # This file
```

## SRT Format

The generated SRT files follow the standard subtitle format:
```
1
00:00:00,000 --> 00:00:03,500
Transcribed text from audio

2
00:00:03,500 --> 00:00:07,200
Next segment of transcribed text
```

## Notes

- The application uses Google's Speech Recognition API which requires an internet connection
- Audio quality affects transcription accuracy
- For best results, use clear audio with minimal background noise
- The Whisper version provides better transcription quality but requires more computational resources

## Troubleshooting

- **FFmpeg not found**: Make sure FFmpeg is installed and added to your system PATH
- **Speech not recognized**: Check audio quality and ensure the audio contains clear speech
- **Network errors**: Verify internet connection for Google Speech Recognition API
- **Memory issues**: For large audio files, the Whisper version may require more RAM
