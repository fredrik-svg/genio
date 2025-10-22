#!/usr/bin/env python3
"""
Test script for Faster Whisper STT initialization
This verifies that the language parameter fix is working correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from stt.faster_whisper import FasterWhisper
from config.settings import STT_MODEL_SIZE, STT_LANGUAGE

def test_stt_initialization():
    """Test STT initialization with language parameter fix"""
    print("=" * 60)
    print("Genio AI - STT Initialization Test")
    print("=" * 60)
    print()
    
    print(f"📋 Configuration:")
    print(f"   Model Size: {STT_MODEL_SIZE}")
    print(f"   Language: {STT_LANGUAGE}")
    print()
    
    print("🔄 Initializing Faster Whisper STT...")
    print("   (This may take a moment on first run to download the model)")
    print()
    
    try:
        stt = FasterWhisper(model_size=STT_MODEL_SIZE, language=STT_LANGUAGE)
        print("✅ SUCCESS! STT initialized without errors!")
        print()
        print("🎉 The language parameter fix is working correctly!")
        print()
        print("Details:")
        print(f"   - Model loaded: {STT_MODEL_SIZE}")
        print(f"   - Language: {stt.language}")
        print(f"   - Device: CPU (CUDA available: {stt._is_cuda_available()})")
        print()
        print("=" * 60)
        print("Next steps:")
        print("1. Configure your Porcupine access key in config/config.yaml")
        print("2. Optionally configure MQTT broker settings")
        print("3. Run: python src/main.py")
        print("=" * 60)
        return True
        
    except TypeError as e:
        if "language" in str(e):
            print("❌ ERROR: Language parameter issue detected!")
            print()
            print("The error suggests the language parameter fix hasn't been applied.")
            print("Make sure src/stt/faster_whisper.py has been updated correctly.")
            print()
            print(f"Error details: {e}")
            return False
        else:
            raise
    
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}")
        print(f"   {e}")
        print()
        print("This is an unexpected error. See TROUBLESHOOTING.md for help.")
        return False

if __name__ == "__main__":
    success = test_stt_initialization()
    sys.exit(0 if success else 1)
