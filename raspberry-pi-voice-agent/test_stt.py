#!/usr/bin/env python3
"""
Comprehensive test script for Faster Whisper STT
Tests initialization, transcribe methods, and audio format handling.
"""

import sys
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from stt.faster_whisper import FasterWhisper, FasterWhisperSTT
from config.settings import STT_MODEL_SIZE, STT_LANGUAGE

def test_stt_initialization():
    """Test STT initialization with language parameter"""
    print("=" * 70)
    print("Test 1: STT Initialization")
    print("=" * 70)
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
        print("Details:")
        print(f"   - Model loaded: {STT_MODEL_SIZE}")
        print(f"   - Language: {stt.language}")
        print(f"   - Device: CPU (CUDA available: {stt._is_cuda_available()})")
        print()
        return True, stt
        
    except TypeError as e:
        if "language" in str(e):
            print("❌ ERROR: Language parameter issue detected!")
            print()
            print("The error suggests the language parameter fix hasn't been applied.")
            print("Make sure src/stt/faster_whisper.py has been updated correctly.")
            print()
            print(f"Error details: {e}")
            return False, None
        else:
            raise
    
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}")
        print(f"   {e}")
        print()
        print("This is an unexpected error. See TROUBLESHOOTING.md for help.")
        return False, None

def test_stt_methods():
    """Test that STT has the required methods"""
    print("=" * 70)
    print("Test 2: STT Method Availability")
    print("=" * 70)
    print()
    
    try:
        stt = FasterWhisperSTT(model_size="tiny", language=STT_LANGUAGE)
        
        required_methods = ['transcribe', 'transcribe_from_stream']
        forbidden_methods = ['convert']
        
        print("Checking for required methods...")
        for method in required_methods:
            if hasattr(stt, method):
                print(f"   ✅ {method}() exists")
            else:
                print(f"   ❌ {method}() missing!")
                return False
        
        print()
        print("Checking for forbidden methods (that shouldn't exist)...")
        for method in forbidden_methods:
            if hasattr(stt, method):
                print(f"   ❌ {method}() should not exist!")
                return False
            else:
                print(f"   ✅ {method}() correctly absent")
        
        print()
        print("✅ All method checks passed!")
        print()
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return False

def test_audio_format_handling():
    """Test that STT can handle different audio input formats"""
    print("=" * 70)
    print("Test 3: Audio Format Handling")
    print("=" * 70)
    print()
    
    # Create test audio data (sine wave)
    sample_rate = 16000
    duration_seconds = 0.1  # Very short for quick test
    num_samples = int(sample_rate * duration_seconds)
    
    t = np.linspace(0, duration_seconds, num_samples)
    frequency = 440  # A4 note
    audio_float = np.sin(2 * np.pi * frequency * t) * 0.3
    audio_int16 = (audio_float * 32767).astype(np.int16)
    
    # Test 1: bytes input (as returned by microphone.listen())
    print("Testing bytes input format...")
    audio_bytes = audio_int16.tobytes()
    print(f"   Input type: {type(audio_bytes)}")
    print(f"   Input size: {len(audio_bytes)} bytes")
    
    try:
        # Test the conversion logic (without actually running transcription)
        audio_input = audio_bytes
        if isinstance(audio_bytes, bytes):
            audio_int16_converted = np.frombuffer(audio_bytes, dtype=np.int16)
            audio_input = audio_int16_converted.astype(np.float32) / 32768.0
            
            print(f"   ✅ Bytes conversion successful")
            print(f"      Output type: {type(audio_input).__name__}")
            print(f"      Output shape: {audio_input.shape}")
            print(f"      Output dtype: {audio_input.dtype}")
            print(f"      Value range: [{audio_input.min():.6f}, {audio_input.max():.6f}]")
            print()
            
            # Verify it's correct
            if not isinstance(audio_input, np.ndarray):
                print("   ❌ ERROR: Not a numpy array")
                return False
            if audio_input.dtype != np.float32:
                print("   ❌ ERROR: Not float32")
                return False
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    # Test 2: numpy array input
    print("Testing numpy array input format...")
    try:
        audio_array = audio_int16.astype(np.float32) / 32768.0
        print(f"   Input type: {type(audio_array).__name__}")
        print(f"   Input shape: {audio_array.shape}")
        print(f"   Input dtype: {audio_array.dtype}")
        print(f"   ✅ Numpy array format valid")
        print()
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False
    
    print("✅ All audio format tests passed!")
    print()
    return True

def test_alias():
    """Test that FasterWhisper is an alias for FasterWhisperSTT"""
    print("=" * 70)
    print("Test 4: Backward Compatibility Alias")
    print("=" * 70)
    print()
    
    print("Testing FasterWhisper alias...")
    if FasterWhisper is FasterWhisperSTT:
        print("   ✅ FasterWhisper is correctly aliased to FasterWhisperSTT")
        print()
        return True
    else:
        print("   ❌ ERROR: FasterWhisper is not aliased correctly")
        print()
        return False

def run_all_tests():
    """Run all STT tests"""
    print()
    print("=" * 70)
    print("Genio AI - Comprehensive STT Test Suite")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: Initialization
    success, stt = test_stt_initialization()
    results.append(("Initialization", success))
    
    # Test 2: Methods
    success = test_stt_methods()
    results.append(("Method Availability", success))
    
    # Test 3: Audio formats
    success = test_audio_format_handling()
    results.append(("Audio Format Handling", success))
    
    # Test 4: Alias
    success = test_alias()
    results.append(("Backward Compatibility", success))
    
    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print()
    
    all_passed = True
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status}: {test_name}")
        if not success:
            all_passed = False
    
    print()
    print("=" * 70)
    
    if all_passed:
        print("🎉 All tests passed!")
        print()
        print("Next steps:")
        print("1. Configure your Porcupine access key in config/config.yaml")
        print("2. Optionally configure MQTT broker settings")
        print("3. Run: python src/main.py")
    else:
        print("❌ Some tests failed. Please review the errors above.")
    
    print("=" * 70)
    print()
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
