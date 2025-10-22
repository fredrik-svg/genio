# Genio AI - Porcupine Wake Word Setup

## Översikt
Genio AI använder Porcupine från Picovoice för wake word detection. Denna guide hjälper dig att konfigurera det.

## Steg 1: Skaffa Porcupine Access Key

1. Gå till [Picovoice Console](https://console.picovoice.ai/)
2. Skapa ett gratis konto
3. Generera en **Access Key** (gratis för personlig användning)
4. Kopiera din Access Key

## Steg 2: Uppdatera konfigurationen

### Metod A: Miljövariabel (Rekommenderat)

Skapa en `.env` fil i projektmappen:

```bash
cd genio/raspberry-pi-voice-agent
nano .env
```

Lägg till:
```env
PORCUPINE_ACCESS_KEY=your_access_key_here
```

### Metod B: Direkt i config.yaml

Redigera `config/config.yaml`:

```yaml
wakeword_detection:
  enabled: true
  access_key: "your_access_key_here"
  keyword: "hej"
  sensitivity: 0.5
```

## Steg 3: Välj Wake Word

Porcupine har flera inbyggda wake words. För svenska rekommenderas:

### Inbyggda wake words (gratis):
- **"hey google"**
- **"alexa"**
- **"hey siri"**
- **"jarvis"**
- **"computer"**
- **"porcupine"**

### Custom wake word (kräver Picovoice konto):
Du kan träna egna wake words (t.ex. "Hej Genio") via Picovoice Console.

## Steg 4: Uppdatera settings.py

Vi behöver uppdatera `src/config/settings.py` för att läsa access key:

```python
import os
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv()

# Porcupine settings
PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY') or config.get('wakeword_detection', {}).get('access_key', '')
```

## Alternativ: Använd Snowboy (Offline, Gratis)

Om du inte vill använda Porcupine (kräver API-nyckel), kan du använda Snowboy istället:

### Installation av Snowboy

```bash
# Installera dependencies
sudo apt-get install swig python3-dev libatlas-base-dev

# Installera snowboy
pip install snowboy
```

### Fördelar med Snowboy:
- ✅ Helt offline
- ✅ Ingen API-nyckel behövs
- ✅ Gratis
- ✅ Custom wake words

### Nackdelar:
- ❌ Lägre precision än Porcupine
- ❌ Projektet är inte längre aktivt underhållet

## Alternativ 2: Använd openWakeWord (Modern, Offline)

Ett modernt alternativ är openWakeWord:

```bash
pip install openwakeword
```

### Fördelar:
- ✅ Helt offline
- ✅ Gratis och open source
- ✅ Modern och aktivt underhållet
- ✅ Flera inbyggda wake words
- ✅ Fungerar bra på Raspberry Pi

## Uppdatera requirements.txt

Välj en av dessa:

### För Porcupine (standardvalet):
```
pvporcupine
```

### För Snowboy:
```
snowboy
```

### För openWakeWord:
```
openwakeword
```

## Test av wake word

Skapa en testfil `test_wakeword.py`:

```python
#!/usr/bin/env python3
import pvporcupine
import pyaudio
import struct
import os
from dotenv import load_dotenv

load_dotenv()

access_key = os.getenv('PORCUPINE_ACCESS_KEY')

if not access_key:
    print("ERROR: PORCUPINE_ACCESS_KEY inte satt!")
    print("Skapa en .env fil med din access key")
    exit(1)

# Använd inbyggt wake word "porcupine"
porcupine = pvporcupine.create(
    access_key=access_key,
    keywords=['porcupine']
)

pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Lyssnar efter wake word 'porcupine'...")
print("Säg 'porcupine' för att testa!")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        
        if keyword_index >= 0:
            print("✅ Wake word detekterat!")
            break
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
    print("Test klart!")
```

Kör testet:
```bash
source genio-env/bin/activate
python test_wakeword.py
```

## Felsökning

### Problem: "Invalid access key"
- Kontrollera att du kopierat hela access key
- Försäkra dig om att det inte finns extra mellanslag
- Verifiera att nyckeln är aktiv på Picovoice Console

### Problem: "No audio input device"
```bash
# Lista ljudenheter
arecord -l

# Testa mikrofon
arecord -d 5 test.wav
aplay test.wav
```

### Problem: PyAudio installation error
```bash
# Installera dependencies först
sudo apt-get install portaudio19-dev python3-pyaudio

# Sedan installera PyAudio
pip install pyaudio
```

## Rekommendation för Genio AI

För bästa resultat rekommenderar vi:

1. **För produktion:** Porcupine med inbyggt wake word "computer" eller "jarvis"
2. **För utveckling:** openWakeWord (gratis, offline)
3. **För custom wake word:** Träna egen modell via Picovoice Console

---

**Genio AI** 🤖
