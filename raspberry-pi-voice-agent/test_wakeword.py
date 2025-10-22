#!/usr/bin/env python3
"""
Genio AI - Wake Word Test
Testar Porcupine wake word detection
"""

import pvporcupine
import pyaudio
import struct
import sys
from pathlib import Path

# Add src to path to import settings
sys.path.insert(0, str(Path(__file__).parent / 'src'))
from config import settings

def main():
    print("🤖 Genio AI - Wake Word Test")
    print("=" * 50)
    
    # Hämta access key från config
    access_key = settings.PORCUPINE_ACCESS_KEY
    
    if not access_key or access_key == "YOUR_PORCUPINE_ACCESS_KEY_HERE":
        print("❌ ERROR: PORCUPINE_ACCESS_KEY inte konfigurerad!")
        print("\nSteg för att fixa:")
        print("1. Gå till https://console.picovoice.ai/")
        print("2. Skapa ett gratis konto")
        print("3. Generera en Access Key")
        print("4. Redigera config/config.yaml:")
        print("   wakeword_detection:")
        print("     access_key: 'din_key_här'")
        return 1
    
    print(f"✅ Access Key hittad: {access_key[:10]}...")
    
    # Wake word att testa
    wake_word = settings.WAKE_WORD
    
    try:
        print(f"\n🔧 Initialiserar Porcupine med wake word: '{wake_word}'")
        
        # Import the PorcupineDetector class
        from wakeword.porcupine_detector import PorcupineDetector
        
        # Create detector instance
        detector = PorcupineDetector(
            access_key=access_key,
            keywords=[wake_word]
        )
        
        # Initialize detector
        detector.initialize()
        
        print(f"\n👂 Lyssnar efter wake word '{wake_word}'...")
        print(f"💡 Tips: Säg '{wake_word}' tydligt!")
        print("🛑 Tryck Ctrl+C för att avsluta\n")
        
        try:
            detected = False
            while not detected:
                if detector.detect():
                    print(f"\n🎉 Wake word '{wake_word}' detekterat!")
                    print("✅ Test godkänt!\n")
                    detected = True
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Test avbrutet av användaren")
            
        finally:
            # Städa upp
            detector.cleanup()
            print("👋 Avslutar...")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nFelsökning:")
        print("- Kontrollera att din access key är giltig")
        print("- Verifiera att mikrofonen fungerar: arecord -d 5 test.wav")
        print("- Se till att PyAudio är korrekt installerat")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
