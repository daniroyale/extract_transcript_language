# SRT Translator Application

A Python application that automatically translates SRT subtitle files from Spanish to English while preserving the SRT format, timestamps, and subtitle numbering.

## Features

- **Automatic Translation**: Uses Google Translate API to translate Spanish text to English
- **Format Preservation**: Maintains SRT file structure, timestamps, and subtitle numbering
- **Batch Processing**: Processes all SRT files in a directory at once
- **Error Handling**: Gracefully handles translation errors and continues processing
- **Flexible Configuration**: Supports custom input/output directories and language codes

## Requirements

- Python 3.7 or higher
- Internet connection (for Google Translate API)
- Required Python packages (see installation section)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements_srt_translator.txt
```

Or install manually:
```bash
pip install googletrans==4.0.0rc1
pip install requests
```

### 2. Verify Installation

```bash
python srt_translator.py --help
```

## Usage

### Basic Usage (Windows)

1. **Double-click** `run_srt_translator.bat` to run the application
2. The application will automatically:
   - Check for required dependencies
   - Install them if needed
   - Process all SRT files in the `srt_spanish` folder
   - Save translated files to the `srt_english` folder

### Command Line Usage

#### Default Behavior
```bash
python srt_translator.py
```
This will:
- Read SRT files from `srt_spanish/` folder
- Translate them to English
- Save translated files to `srt_english/` folder

#### Custom Directories
```bash
python srt_translator.py --input my_spanish_subs --output my_english_subs
```

#### Custom Languages
```bash
# Translate from Portuguese to English
python srt_translator.py --source-lang pt --target-lang en

# Translate from Spanish to French
python srt_translator.py --source-lang es --target-lang fr
```

#### Command Line Options
```bash
python srt_translator.py --help
```

Available options:
- `--input, -i`: Input directory (default: `srt_spanish`)
- `--output, -o`: Output directory (default: `srt_english`)
- `--source-lang, -s`: Source language code (default: `es`)
- `--target-lang, -t`: Target language code (default: `en`)

## Directory Structure

```
transcript_language/
├── srt_spanish/          # Input: Spanish SRT files
│   ├── que_puedo_hacer_por_ti.srt
│   └── other_files.srt
├── srt_english/          # Output: English SRT files
│   ├── que_puedo_hacer_por_ti.srt
│   └── other_files.srt
├── srt_translator.py     # Main application
├── requirements_srt_translator.txt
├── run_srt_translator.bat
└── README_SRT_Translator.md
```

## How It Works

1. **File Discovery**: Scans the input directory for `.srt` files
2. **Parsing**: Parses each SRT file to extract:
   - Subtitle index numbers
   - Timestamps
   - Subtitle text
3. **Translation**: Translates only the subtitle text using Google Translate
4. **Reconstruction**: Rebuilds the SRT file with translated text while preserving:
   - Original index numbers
   - Exact timestamps
   - File structure and formatting
5. **Output**: Saves translated files to the output directory

## Example Output

### Input (Spanish SRT)
```
1
00:00:00,000 --> 00:00:12,480
Que bueno verdad, poder entender lo que Dios hace en nuestras vidas
```

### Output (English SRT)
```
1
00:00:00,000 --> 00:00:12,480
How good it is, to be able to understand what God does in our lives
```

## Troubleshooting

### Common Issues

1. **"No translation service available"**
   - Install the required package: `pip install googletrans==4.0.0rc1`
   - Ensure you have an internet connection

2. **Translation errors**
   - Check your internet connection
   - Google Translate may have rate limits
   - The application will continue processing other files

3. **File encoding issues**
   - SRT files should be in UTF-8 encoding
   - The application handles encoding automatically

4. **Permission errors**
   - Ensure you have write permissions to the output directory
   - Run as administrator if needed (Windows)

### Performance Tips

- **Large files**: The application processes files sequentially to avoid overwhelming the translation service
- **Batch processing**: Process multiple files at once rather than running the application multiple times
- **Internet connection**: Stable internet connection improves translation reliability

## Supported Languages

The application supports all languages available through Google Translate. Common language codes:

- `es` - Spanish
- `en` - English
- `fr` - French
- `de` - German
- `pt` - Portuguese
- `it` - Italian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese
- `ar` - Arabic

## Limitations

- **Translation Quality**: Depends on Google Translate's accuracy
- **Rate Limits**: Google Translate may have usage limits
- **Internet Required**: Requires active internet connection
- **File Size**: Very large SRT files may take longer to process

## Contributing

Feel free to improve the application by:
- Adding support for other translation services
- Implementing batch translation with progress bars
- Adding support for other subtitle formats
- Improving error handling and user feedback

## License

This application is provided as-is for educational and personal use.

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify your internet connection
4. Check that input files are valid SRT format
