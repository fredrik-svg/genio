# Genio AI - Fix för PorcupineDetector TypeError

## Problem
```
TypeError: PorcupineDetector.__init__() missing 1 required positional argument: 'keyword_paths'
```

## Orsak
`PorcupineDetector` hade fel signatur och förväntade sig både `access_key` och `keyword_paths`, men main.py skickade bara `WAKE_WORD`.

## Lösning ✅

### 1. Omskrivit PorcupineDetector
**Fil:** `src/wakeword/porcupine_detector.py`

**Nya funktioner:**
- ✅ Stödjer både inbyggda keywords (`keywords=['porcupine']`) och custom .ppn-filer (`keyword_paths=['model.ppn']`)
- ✅ Tar access_key som första argument
- ✅ Bättre felhantering och loggning
- ✅ Context manager support (`with` statement)
- ✅ Automatisk initialisering vid första detect()

**Ny signatur:**
```python
PorcupineDetector(
    access_key,           # Porcupine API key (required)
    keywords=None,        # Built-in keywords: ['porcupine', 'alexa', etc]
    keyword_paths=None,   # Custom .ppn files: ['model.ppn']
    sensitivity=0.5       # Detection sensitivity 0.0-1.0
)
```

### 2. Uppdaterat main.py
**Fil:** `src/main.py`

**Ändringar:**
- ✅ Importerar nu `PORCUPINE_ACCESS_KEY`, `WAKE_WORD_SENSITIVITY`, `WAKE_WORD_MODEL_PATH`
- ✅ Validerar att access key finns innan start
- ✅ Skapar PorcupineDetector korrekt med access key
- ✅ Stödjer både inbyggda keywords och custom .ppn-filer
- ✅ Bättre loggning under initialisering

**Exempel:**
```python
# För inbyggt keyword (standard)
self.porcupine_detector = PorcupineDetector(
    access_key=PORCUPINE_ACCESS_KEY,
    keywords=[WAKE_WORD],  # e.g., 'porcupine'
    sensitivity=WAKE_WORD_SENSITIVITY
)

# För custom .ppn fil
self.porcupine_detector = PorcupineDetector(
    access_key=PORCUPINE_ACCESS_KEY,
    keyword_paths=[WAKE_WORD_MODEL_PATH],
    sensitivity=WAKE_WORD_SENSITIVITY
)
```

### 3. Uppdaterat test_wakeword.py
**Fil:** `test_wakeword.py`

**Ändringar:**
- ✅ Använder nu PorcupineDetector-klassen
- ✅ Bättre felhantering
- ✅ Automatisk cleanup

### 4. Förbättrat Logger
**Fil:** `src/utils/logger.py`

**Ändringar:**
- ✅ Läser LOG_LEVEL och LOG_FILE från miljövariabler
- ✅ Skapar logs-mapp automatiskt
- ✅ Både console och file logging
- ✅ Undviker duplicerade handlers
- ✅ Bättre formatering

### 5. Uppdaterat settings.py
**Ändringar:**
- ✅ Exporterar `WAKE_WORD_SENSITIVITY`
- ✅ Bättre felmeddelande om access key saknas

## Hur man använder nu

### 1. Konfigurera (config.yaml)
```yaml
wakeword_detection:
  enabled: true
  access_key: "din_porcupine_key"  # Från console.picovoice.ai
  keyword: "porcupine"              # Inbyggda: porcupine, alexa, computer, jarvis
  sensitivity: 0.5
  model_path: ""                    # Tom om du använder inbyggt keyword
```



### 2. Testa wake word
```bash
source genio-env/bin/activate
python test_wakeword.py
```

Säg "porcupine" (eller ditt valda keyword).

### 3. Kör Genio AI
```bash
source genio-env/bin/activate
python src/main.py
```

## Inbyggda Wake Words (gratis med Porcupine)

Du kan använda dessa keywords utan extra konfiguration:
- `porcupine` ✅ (standard i Genio AI)
- `alexa`
- `computer`
- `jarvis`
- `hey google`
- `hey siri`
- `ok google`
- `picovoice`
- `bumblebee`
- `grapefruit`
- `grasshopper`
- `terminator`

Ändra i config.yaml:
```yaml
wakeword_detection:
  keyword: "computer"  # Välj vilket du vill
```

## Custom Wake Words

Om du vill använda egna wake words (t.ex. "Hej Genio"):

1. Gå till [Picovoice Console](https://console.picovoice.ai/)
2. Träna en custom wake word model
3. Ladda ner .ppn-filen
4. Konfigurera:

```yaml
wakeword_detection:
  access_key: "din_key"
  keyword: ""  # Lämna tom
  model_path: "models/hej-genio.ppn"  # Path till din .ppn fil
```

## Felsökning

### Problem: "Invalid access key"
```bash
# Kontrollera att key är korrekt satt
python -c "from src.config.settings import PORCUPINE_ACCESS_KEY; print(PORCUPINE_ACCESS_KEY[:10] + '...' if PORCUPINE_ACCESS_KEY else 'NOT SET')"
```

### Problem: "No audio input device"
```bash
# Lista ljudenheter
python -c "import pyaudio; pa = pyaudio.PyAudio(); [print(f'[{i}] {pa.get_device_info_by_index(i)[\"name\"]}') for i in range(pa.get_device_count()) if pa.get_device_info_by_index(i)['maxInputChannels'] > 0]"
```

### Problem: Wake word detekteras inte
- Öka sensitivity i config: `sensitivity: 0.7`
- Prata tydligare och närmare mikrofonen
- Kontrollera att rätt mikrofon används

## Validera Installation

Kör alla tester:
```bash
source genio-env/bin/activate

# 1. Testa wake word
python test_wakeword.py

# 2. Testa TTS
python test_piper.py

# 3. Verifiera konfiguration
python -c "
from src.config import settings
print('✅ Porcupine Key:', 'SET' if settings.PORCUPINE_ACCESS_KEY else '❌ NOT SET')
print('✅ Wake Word:', settings.WAKE_WORD)
print('✅ MQTT Broker:', settings.MQTT_BROKER)
print('✅ MQTT Port:', settings.MQTT_PORT)
"

# 4. Kör Genio AI
python src/main.py
```

## Sammanfattning av Ändringar

### Modifierade Filer:
1. ✅ `src/wakeword/porcupine_detector.py` - Komplett omskrivning
2. ✅ `src/main.py` - Uppdaterad PorcupineDetector-användning
3. ✅ `src/utils/logger.py` - Förbättrad logging
4. ✅ `test_wakeword.py` - Använder nya PorcupineDetector
5. ✅ `src/config/settings.py` - Exporterar alla nödvändiga variabler

### Nya Funktioner:
- ✅ Stöd för både inbyggda och custom keywords
- ✅ Bättre felhantering och validering
- ✅ Context manager för säker resurshantering
- ✅ Automatisk logs-mapp skapande
- ✅ Förbättrad loggning genom hela systemet

### Bakåtkompatibilitet:
- ✅ Gamla konfigurationsfiler fungerar fortfarande
- ✅ Standardvärden för alla inställningar

---

**Status:** ✅ **ALLA PROBLEM FIXADE!**

Nu kan du köra:
```bash
python src/main.py
```

**Genio AI** 🤖 - Redo att använda!
