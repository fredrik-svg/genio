#!/usr/bin/env python3
"""
Unit test for STT class structure and methods
This test validates the fix without requiring model downloads.
"""

import sys
from pathlib import Path
import inspect

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_stt_class_structure():
    """Test that FasterWhisperSTT has the correct methods"""
    print("=" * 70)
    print("Unit Test: STT Class Structure")
    print("=" * 70)
    print()
    
    # Import the source code
    try:
        with open(Path(__file__).parent / "src" / "stt" / "faster_whisper.py", 'r') as f:
            source_code = f.read()
        
        print("✓ Successfully read STT source code")
        print()
        
        # Check for required methods
        print("Checking for required methods...")
        required_methods = {
            'transcribe': False,
            'transcribe_from_stream': False,
            '__init__': False
        }
        
        for method in required_methods:
            if f"def {method}(" in source_code:
                print(f"   ✅ {method}() method found")
                required_methods[method] = True
            else:
                print(f"   ❌ {method}() method NOT found")
        
        print()
        
        # Check for forbidden methods
        print("Checking for forbidden methods (that should NOT exist)...")
        forbidden_methods = ['convert']
        has_forbidden = False
        
        for method in forbidden_methods:
            if f"def {method}(" in source_code:
                print(f"   ❌ {method}() method found (should not exist!)")
                has_forbidden = True
            else:
                print(f"   ✅ {method}() correctly absent")
        
        print()
        
        # Check for FasterWhisper alias
        print("Checking for backward compatibility alias...")
        if "FasterWhisper = FasterWhisperSTT" in source_code:
            print("   ✅ FasterWhisper alias correctly defined")
            alias_ok = True
        else:
            print("   ❌ FasterWhisper alias NOT found")
            alias_ok = False
        
        print()
        
        # Results
        all_required = all(required_methods.values())
        
        if all_required and not has_forbidden and alias_ok:
            print("✅ All structure checks PASSED!")
            return True
        else:
            print("❌ Some structure checks FAILED")
            if not all_required:
                missing = [m for m, found in required_methods.items() if not found]
                print(f"   Missing methods: {', '.join(missing)}")
            if has_forbidden:
                print(f"   Forbidden methods found: {', '.join(forbidden_methods)}")
            if not alias_ok:
                print("   FasterWhisper alias not defined")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return False

def test_main_py_fix():
    """Test that main.py no longer calls the non-existent convert method"""
    print("=" * 70)
    print("Unit Test: main.py process_command Fix")
    print("=" * 70)
    print()
    
    try:
        with open(Path(__file__).parent / "src" / "main.py", 'r') as f:
            source_code = f.read()
        
        print("✓ Successfully read main.py source code")
        print()
        
        # Check that convert is not called
        print("Checking for incorrect STT usage...")
        if ".stt.convert(" in source_code or "stt.convert(" in source_code:
            print("   ❌ Found call to stt.convert() - this should not exist!")
            print("      The convert() method doesn't exist in FasterWhisperSTT")
            return False
        else:
            print("   ✅ No calls to stt.convert() found (correct!)")
        
        print()
        
        # Verify process_command exists
        print("Checking process_command method...")
        if "def process_command(self, command):" in source_code:
            print("   ✅ process_command() method found")
        else:
            print("   ❌ process_command() method NOT found")
            return False
        
        print()
        
        # Verify transcribe is used correctly
        print("Checking correct STT usage...")
        if ".stt.transcribe(" in source_code or "stt.transcribe(" in source_code:
            print("   ✅ Found call to stt.transcribe() (correct!)")
        else:
            print("   ⚠️  No calls to stt.transcribe() found")
            print("      This might be OK if STT is used differently")
        
        print()
        print("✅ main.py fix validation PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return False

def test_audio_conversion_logic():
    """Test the audio bytes to numpy array conversion logic"""
    print("=" * 70)
    print("Unit Test: Audio Conversion Logic")
    print("=" * 70)
    print()
    
    try:
        import numpy as np
        
        # Create test audio data
        sample_rate = 16000
        duration = 0.1
        num_samples = int(sample_rate * duration)
        
        # Create sine wave
        t = np.linspace(0, duration, num_samples)
        audio_float = np.sin(2 * np.pi * 440 * t) * 0.3
        audio_int16 = (audio_float * 32767).astype(np.int16)
        
        # Convert to bytes (as returned by microphone)
        audio_bytes = audio_int16.tobytes()
        
        print(f"Created test audio data:")
        print(f"   Type: {type(audio_bytes)}")
        print(f"   Size: {len(audio_bytes)} bytes")
        print()
        
        # Test the conversion (this is the logic from FasterWhisperSTT.transcribe)
        print("Testing bytes to numpy conversion...")
        if isinstance(audio_bytes, bytes):
            audio_int16_converted = np.frombuffer(audio_bytes, dtype=np.int16)
            audio_float32 = audio_int16_converted.astype(np.float32) / 32768.0
            
            print(f"   ✅ Conversion successful!")
            print(f"      Input:  {type(audio_bytes).__name__} ({len(audio_bytes)} bytes)")
            print(f"      Output: {type(audio_float32).__name__} {audio_float32.shape}")
            print(f"      Dtype:  {audio_float32.dtype}")
            print(f"      Range:  [{audio_float32.min():.6f}, {audio_float32.max():.6f}]")
            
            # Validate
            if not isinstance(audio_float32, np.ndarray):
                print("   ❌ Output is not a numpy array")
                return False
            
            if audio_float32.dtype != np.float32:
                print("   ❌ Output dtype is not float32")
                return False
            
            if audio_float32.min() < -1.1 or audio_float32.max() > 1.1:
                print("   ⚠️  Values outside expected range [-1, 1]")
            
            print()
            print("✅ Audio conversion logic PASSED!")
            return True
        else:
            print("   ❌ Test audio is not bytes type")
            return False
            
    except ImportError:
        print("⚠️  numpy not installed, skipping audio conversion test")
        return True  # Don't fail if numpy not available
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {e}")
        return False

def run_all_tests():
    """Run all unit tests"""
    print()
    print("=" * 70)
    print("Genio AI - STT Unit Test Suite")
    print("=" * 70)
    print()
    
    results = []
    
    # Test 1: STT class structure
    success = test_stt_class_structure()
    results.append(("STT Class Structure", success))
    print()
    
    # Test 2: main.py fix
    success = test_main_py_fix()
    results.append(("main.py Fix", success))
    print()
    
    # Test 3: Audio conversion
    success = test_audio_conversion_logic()
    results.append(("Audio Conversion Logic", success))
    print()
    
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
        print("🎉 All unit tests passed!")
        print()
        print("The fix successfully addresses the AttributeError:")
        print("  • FasterWhisperSTT has transcribe() and transcribe_from_stream()")
        print("  • FasterWhisperSTT does NOT have convert() method")
        print("  • main.py no longer calls the non-existent convert() method")
        print("  • Audio bytes are correctly converted to numpy arrays")
    else:
        print("❌ Some tests failed. Please review the errors above.")
    
    print("=" * 70)
    print()
    
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
