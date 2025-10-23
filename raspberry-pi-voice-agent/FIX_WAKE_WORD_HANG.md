# Fix: Wake Word Detection Hang

## Problem

Efter att wake word detekterades hängde systemet och ingenting hände. Användaren var tvungen att manuellt avbryta med Ctrl+C, vilket orsakade följande fel:

```
KeyboardInterrupt
  File "/home/genio/apps/genio/raspberry-pi-voice-agent/src/main.py", line 119, in listen_for_wake_word
    command = self.stt.transcribe(audio)
  File "/home/genio/apps/genio/raspberry-pi-voice-agent/src/stt/faster_whisper.py", line 25, in transcribe
    return " ".join(segment.text for segment in segments)
```

## Orsak

Problemet var att `microphone.listen()` använde en oändlig loop som bara stoppades av `KeyboardInterrupt`:

```python
# GAMMALT (felaktigt):
def listen(self):
    frames = []
    try:
        while True:  # ❌ Oändlig loop!
            data = self.stream.read(self.chunk)
            frames.append(data)
    except KeyboardInterrupt:
        print("Recording stopped.")
        self.stop()
    return b''.join(frames)
```

Detta innebar att:
1. Efter wake word-detektering började systemet spela in
2. Inspelningen fortsatte i oändlighet
3. Användaren var tvungen att trycka Ctrl+C för att stoppa
4. KeyboardInterrupt propagerade genom transkriptionen
5. Hela systemet kraschade

## Lösning

### 1. Tidsbegränsad inspelning

Mikrofonen spelar nu in under en fast tidsperiod (standard 5 sekunder):

```python
# NYTT (korrekt):
def listen(self, duration=None):
    """
    Record audio for a specified duration.
    
    Args:
        duration: Recording duration in seconds. If None, uses self.record_seconds.
    
    Returns:
        bytes: Recorded audio data
    """
    if duration is None:
        duration = self.record_seconds
        
    frames = []
    num_chunks = int(self.rate / self.chunk * duration)
    
    try:
        print(f"🎤 Recording for {duration} seconds...")
        for i in range(num_chunks):  # ✅ Fast längd!
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)
        print("✅ Recording complete!")
    except KeyboardInterrupt:
        print("⚠️  Recording stopped by user.")
    
    return b''.join(frames)
```

### 2. Konfigurerbar inspelningstid

Ny konfiguration i `config/config.yaml`:

```yaml
audio:
  record_seconds: 5  # Hur många sekunder att spela in efter wake word
```

Du kan justera detta värde baserat på dina behov:
- **3 sekunder**: För korta kommandon ("tända lampan")
- **5 sekunder**: Rekommenderat för normala kommandon
- **10 sekunder**: För längre fraser eller meningar

### 3. Förbättrad felhantering

`main.py` har nu bättre felhantering:

```python
def listen_for_wake_word(self):
    try:
        while True:
            if self.porcupine_detector.detect():
                self.logger.info("Wake word detected!")
                try:
                    audio = self.microphone.listen()
                    self.logger.info("Transcribing audio...")
                    command = self.stt.transcribe(audio)
                    self.logger.info(f"Transcribed command: {command}")
                    
                    # Process command...
                except KeyboardInterrupt:
                    raise  # Re-raise to outer handler
                except Exception as e:
                    self.logger.error(f"Error processing command: {e}")
                    self.speaker.speak("Ursäkta, jag kunde inte förstå det.")
    except KeyboardInterrupt:
        self.logger.info("🛑 Genio AI stopped by user")
        # Clean up resources...
```

## Användning

### Standard användning (5 sekunder)

Efter uppdateringen fungerar systemet automatiskt:

```bash
python src/main.py
# Säg wake word
# 🎤 Recording for 5 seconds...
# ✅ Recording complete!
# Transcribing audio...
```

### Anpassad inspelningstid

Redigera `config/config.yaml`:

```yaml
audio:
  record_seconds: 8  # Ändra till 8 sekunder
```

### Programmatisk användning

```python
from audio.microphone import Microphone

# Skapa mikrofon med 7 sekunders standard
mic = Microphone(record_seconds=7)

# Spela in med standard (7 sekunder)
audio = mic.listen()

# Spela in med custom duration (3 sekunder)
audio = mic.listen(duration=3)
```

## Fördelar

✅ **Inget hängande**: Systemet stannar inte längre efter wake word
✅ **Ingen manuell avbrotning**: Ingen Ctrl+C behövs
✅ **Konfigurerbart**: Justera inspelningstiden efter behov
✅ **Bättre felhantering**: Tydliga felmeddelanden och återhämtning
✅ **Bättre användarupplevelse**: Visuell feedback under inspelning

## Testning

Kör testerna för att verifiera att allt fungerar:

```bash
# Test av microphone duration fix
python test_microphone_duration.py

# Test av STT-systemet
python test_stt_unit.py
```

Alla tester ska passera:

```
🎉 All tests passed!

The microphone duration fix successfully:
  • Removes infinite loop in microphone.listen()
  • Adds configurable recording duration
  • Provides proper KeyboardInterrupt handling
  • Allows system to continue after wake word detection
```

## Backward Compatibility

Ändringen är bakåtkompatibel:
- Befintlig kod fungerar utan ändringar
- `duration` parametern är valfri
- Standard-värdet (5 sekunder) är rimligt för de flesta användningsfall

## Relaterade Filer

Ändrade filer:
- `src/audio/microphone.py` - Tidsbegränsad inspelning
- `config/config.yaml` - Audio-konfiguration
- `src/config/settings.py` - AUDIO_RECORD_SECONDS
- `src/main.py` - Förbättrad felhantering
- `test_microphone_duration.py` - Nya tester (nytt)

## Support

Om du fortfarande har problem:

1. Kontrollera att du har den senaste versionen:
   ```bash
   git pull origin main
   ```

2. Verifiera konfigurationen:
   ```bash
   cat config/config.yaml | grep -A2 "audio:"
   ```

3. Kör testerna:
   ```bash
   python test_microphone_duration.py
   python test_stt_unit.py
   ```

4. Aktivera debug-loggning i `config/config.yaml`:
   ```yaml
   logging:
     level: "DEBUG"
   ```

---

**Genio AI** 🤖 - Din intelligenta röstassistent
