#!/usr/bin/env python3
"""
Simple test script for Piper TTS functionality.
Run this to verify that Piper TTS is working correctly.
"""

from src.tts.tts_engine import PiperTTS
from src.config.settings import TTS_MODEL_PATH, TTS_CONFIG_PATH, TTS_LANGUAGE


def main():
    print("Initializing Piper TTS...")
    try:
        # Initialize Piper TTS
        tts = PiperTTS(
            model_path=TTS_MODEL_PATH,
            config_path=TTS_CONFIG_PATH,
            language=TTS_LANGUAGE
        )
        print("✓ Piper TTS initialized successfully!")
        
        # Test Swedish text
        test_text = "Hej! Detta är ett test av Piper text-till-tal-systemet."
        print(f"\nSpeaking: '{test_text}'")
        
        # Speak the text
        tts.speak(test_text)
        print("✓ Speech completed!")
        
        # Test saving to file
        output_file = "test_output.wav"
        print(f"\nSaving to file: {output_file}")
        tts.save_to_file(test_text, output_file)
        print(f"✓ Audio saved to {output_file}")
        
        print("\n✓ All tests passed!")
        
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        print("\nMake sure you have:")
        print("1. Installed Piper TTS")
        print("2. Downloaded the Swedish voice model")
        print("3. Updated the paths in config/config.yaml")
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
