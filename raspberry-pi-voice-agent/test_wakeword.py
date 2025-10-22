#!/usr/bin/env python3
"""
Genio AI - Wake Word Test
Testar Porcupine wake word detection
"""

import pvporcupine
import pyaudio
import struct
import os
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv()

def main():
    print("🤖 Genio AI - Wake Word Test")
    print("=" * 50)
    
    # Hämta access key
    access_key = os.getenv('PORCUPINE_ACCESS_KEY')
    
    if not access_key:
        print("❌ ERROR: PORCUPINE_ACCESS_KEY inte satt!")
        print("\nSteg för att fixa:")
        print("1. Gå till https://console.picovoice.ai/")
        print("2. Skapa ett gratis konto")
        print("3. Generera en Access Key")
        print("4. Kopiera .env.example till .env:")
        print("   cp .env.example .env")
        print("5. Redigera .env och lägg till din key:")
        print("   PORCUPINE_ACCESS_KEY=din_key_här")
        return 1
    
    print(f"✅ Access Key hittad: {access_key[:10]}...")
    
    # Wake word att testa (använd inbyggda keywords)
    wake_word = os.getenv('WAKE_WORD', 'porcupine')
    
    try:
        print(f"\n🔧 Initialiserar Porcupine med wake word: '{wake_word}'")
        
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=[wake_word]
        )
        
        print(f"✅ Porcupine initialiserad!")
        print(f"   Sample Rate: {porcupine.sample_rate} Hz")
        print(f"   Frame Length: {porcupine.frame_length}")
        
        # Initiera PyAudio
        pa = pyaudio.PyAudio()
        
        # Hitta mikrofon
        print(f"\n🎤 Tillgängliga ljudenheter:")
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"   [{i}] {info['name']}")
        
        # Öppna ljudström
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        print(f"\n👂 Lyssnar efter wake word '{wake_word}'...")
        print(f"💡 Tips: Säg '{wake_word}' tydligt!")
        print("🛑 Tryck Ctrl+C för att avsluta\n")
        
        try:
            while True:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                
                if keyword_index >= 0:
                    print(f"\n🎉 Wake word '{wake_word}' detekterat!")
                    print("✅ Test godkänt!\n")
                    break
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Test avbrutet av användaren")
            
        finally:
            # Städa upp
            audio_stream.close()
            pa.terminate()
            porcupine.delete()
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
