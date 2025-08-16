#!/usr/bin/env python3
"""
SRT Translator Application
Reads SRT files from srt_spanish folder, translates them to English,
and saves the translated files to srt_english folder while preserving the SRT format.

-o srt_portugues -t pt
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import argparse

try:
    from googletrans import Translator
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class SRTTranslator:
    """Class to handle SRT file translation while preserving format."""
    
    def __init__(self, source_lang: str = 'es', target_lang: str = 'en'):
        """
        Initialize the SRT translator.
        
        Args:
            source_lang: Source language code (default: 'es' for Spanish)
            target_lang: Target language code (default: 'en' for English)
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translator = None
        
        # Try to initialize Google Translate
        if GOOGLE_TRANSLATE_AVAILABLE:
            try:
                self.translator = Translator()
                print("✓ Google Translate initialized successfully")
            except Exception as e:
                print(f"⚠ Warning: Could not initialize Google Translate: {e}")
                self.translator = None
        
        if not self.translator:
            print("⚠ No translation service available. Install googletrans==4.0.0rc1")
            print("  pip install googletrans==4.0.0rc1")
    
    def parse_srt(self, content: str) -> List[Tuple[int, str, str, str]]:
        """
        Parse SRT content into structured format.
        
        Args:
            content: Raw SRT file content
            
        Returns:
            List of tuples: (index, timestamp, text, empty_line)
        """
        # Split content into subtitle blocks
        blocks = re.split(r'\n\s*\n', content.strip())
        subtitles = []
        
        for block in blocks:
            if not block.strip():
                continue
                
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    index = int(lines[0])
                    timestamp = lines[1]
                    text = '\n'.join(lines[2:])
                    empty_line = ''
                    subtitles.append((index, timestamp, text, empty_line))
                except ValueError:
                    # Skip malformed blocks
                    continue
        
        return subtitles
    
    def translate_text(self, text: str) -> str:
        """
        Translate text using available translation service.
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        if not self.translator:
            return text  # Return original if no translator available
        
        try:
            # Clean up text for translation
            clean_text = text.strip()
            if not clean_text:
                return text
            
            # Translate the text
            result = self.translator.translate(
                clean_text, 
                src=self.source_lang, 
                dest=self.target_lang
            )
            
            return result.text
            
        except Exception as e:
            print(f"⚠ Translation error: {e}")
            return text  # Return original text on error
    
    def translate_srt_content(self, content: str) -> str:
        """
        Translate SRT content while preserving format.
        
        Args:
            content: Original SRT content
            
        Returns:
            Translated SRT content
        """
        subtitles = self.parse_srt(content)
        translated_blocks = []
        
        for index, timestamp, text, empty_line in subtitles:
            # Translate the subtitle text
            translated_text = self.translate_text(text)
            
            # Reconstruct the block
            block = f"{index}\n{timestamp}\n{translated_text}"
            translated_blocks.append(block)
        
        # Join blocks with double newlines
        return '\n\n'.join(translated_blocks) + '\n'
    
    def translate_file(self, input_file: Path, output_file: Path) -> bool:
        """
        Translate a single SRT file.
        
        Args:
            input_file: Path to input SRT file
            output_file: Path to output SRT file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Translating: {input_file.name}")
            
            # Read input file
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Translate content
            translated_content = self.translate_srt_content(content)
            
            # Ensure output directory exists
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write translated content
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"✓ Saved: {output_file.name}")
            return True
            
        except Exception as e:
            print(f"✗ Error translating {input_file.name}: {e}")
            return False
    
    def translate_directory(self, input_dir: Path, output_dir: Path) -> Tuple[int, int]:
        """
        Translate all SRT files in a directory.
        
        Args:
            input_dir: Input directory containing SRT files
            output_dir: Output directory for translated files
            
        Returns:
            Tuple of (successful_translations, total_files)
        """
        if not input_dir.exists():
            print(f"✗ Input directory does not exist: {input_dir}")
            return 0, 0
        
        # Find all SRT files
        srt_files = list(input_dir.glob("*.srt"))
        
        if not srt_files:
            print(f"ℹ No SRT files found in {input_dir}")
            return 0, 0
        
        print(f"Found {len(srt_files)} SRT files to translate")
        print(f"Input: {input_dir}")
        print(f"Output: {output_dir}")
        print("-" * 50)
        
        successful = 0
        total = len(srt_files)
        
        for srt_file in srt_files:
            # Create output file path
            output_file = output_dir / srt_file.name
            
            # Translate the file
            if self.translate_file(srt_file, output_file):
                successful += 1
        
        return successful, total


def main():
    """Main function to run the SRT translator."""
    parser = argparse.ArgumentParser(
        description="Translate SRT files from Spanish to English while preserving format"
    )
    parser.add_argument(
        "--input", "-i",
        default="srt_spanish",
        help="Input directory containing Spanish SRT files (default: srt_spanish)"
    )
    parser.add_argument(
        "--output", "-o", 
        default="srt_english",
        help="Output directory for English SRT files (default: srt_english)"
    )
    parser.add_argument(
        "--source-lang", "-s",
        default="es",
        help="Source language code (default: es)"
    )
    parser.add_argument(
        "--target-lang", "-t",
        default="en", 
        help="Target language code (default: en)"
    )
    
    args = parser.parse_args()
    
    # Convert to Path objects
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    # Check if input directory exists
    if not input_dir.exists():
        print(f"✗ Input directory does not exist: {input_dir}")
        print("Please create the directory or specify a different path with --input")
        sys.exit(1)
    
    # Create translator instance
    translator = SRTTranslator(
        source_lang=args.source_lang,
        target_lang=args.target_lang
    )
    
    # Check if translation service is available
    if not translator.translator:
        print("\n⚠ No translation service available!")
        print("To use this application, install the required package:")
        print("pip install googletrans==4.0.0rc1")
        print("\nAlternatively, you can manually translate the files.")
        sys.exit(1)
    
    # Translate all files
    successful, total = translator.translate_directory(input_dir, output_dir)
    
    # Print summary
    print("-" * 50)
    if successful == total:
        print(f"✓ Successfully translated all {total} files!")
    else:
        print(f"⚠ Translated {successful} out of {total} files")
        print(f"✗ Failed to translate {total - successful} files")
    
    print(f"Output directory: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
