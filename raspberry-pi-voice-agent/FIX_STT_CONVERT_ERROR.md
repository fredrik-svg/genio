# Fix för AttributeError: 'FasterWhisperSTT' object has no attribute 'convert'

## Problem
Applikationen kraschade med följande fel när ett kommando togs emot via MQTT:

```
AttributeError: 'FasterWhisperSTT' object has no attribute 'convert'
```

Felet uppstod i `src/main.py` på rad 109 i metoden `process_command()`.

## Orsak
Metoden `process_command()` försökte anropa `self.stt.convert(command)`, men:
1. Klassen `FasterWhisperSTT` har ingen `convert()` metod
2. STT (Speech-to-Text) används för att konvertera ljud till text, inte text till text
3. `process_command()` tar emot textkommandon från MQTT, inte ljud

## Lösning
### 1. Fixade main.py
Uppdaterade `process_command()` metoden att:
- Ta bort det felaktiga anropet till `self.stt.convert(command)`
- Logga inkommande kommandon korrekt
- Svara genom att upprepa kommandot ("Mottaget kommando: {command}")

**Före:**
```python
def process_command(self, command):
    # Process the command and respond accordingly
    response = self.stt.convert(command)
    self.speaker.speak(response)
```

**Efter:**
```python
def process_command(self, command):
    # Process the command and respond accordingly
    self.logger.info(f"Processing command: {command}")
    # Echo the command back to confirm receipt
    response = f"Mottaget kommando: {command}"
    self.speaker.speak(response)
```

### 2. Skapade omfattande tester
Skapade två testfiler:

#### test_stt.py (Uppdaterad)
Omfattande tester för STT-funktionalitet:
- ✅ STT initialisering med språkparameter
- ✅ Metodtillgänglighet (transcribe, transcribe_from_stream)
- ✅ Audioformat hantering
- ✅ Bakåtkompatibilitet alias

#### test_stt_unit.py (Ny)
Enhetstester som inte kräver modellnedladdning:
- ✅ STT klassstruktur validering
- ✅ main.py fix validering
- ✅ Audio konverteringslogik tester

Alla tester körs utan att kräva installation av alla beroenden.

## Verifiering
Kör testerna för att verifiera fixet:

```bash
# Enhetstester (kräver bara numpy)
python test_stt_unit.py

# Audio bytes test
python test_audio_bytes.py

# Fullständiga STT tester (kräver faster-whisper)
python test_stt.py
```

## Resultat
- ✅ AttributeError fixat
- ✅ MQTT kommandohantering fungerar
- ✅ Omfattande tester tillagda
- ✅ Inga säkerhetsproblem (CodeQL ren)

## Tekniska detaljer

### Korrekta STT-metoder
`FasterWhisperSTT` klassen har följande metoder:
- `transcribe(audio_file)` - Transkriberar ljud (bytes eller numpy array) till text
- `transcribe_from_stream(audio_stream)` - Transkriberar från ljudström
- `__init__(model_size, language)` - Initialiserar modellen

### Korrekta användning av STT
STT används korrekt i `listen_for_wake_word()`:
```python
audio = self.microphone.listen()
command = self.stt.transcribe(audio)  # ✅ Korrekt: ljud → text
```

### Flöde
1. Vakord detekteras → `porcupine_detector.detect()`
2. Ljud spelas in → `microphone.listen()` returnerar bytes
3. Ljud transkriberas → `stt.transcribe(audio)` returnerar text
4. Kommando publiceras → MQTT topic "genio/commands"
5. Kommando tas emot → `on_message()` callback
6. Kommando behandlas → `process_command()` svarar

## Framtida förbättringar
I framtiden kan `process_command()` utökas att:
- Tolka specifika kommandon (t.ex. "tänd lampan", "stäng av")
- Integrera med hemautomation
- Använda AI för att generera mer intelligenta svar
