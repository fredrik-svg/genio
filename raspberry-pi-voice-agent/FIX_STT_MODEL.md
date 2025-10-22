# Genio AI - Fix för STT Model Error

## Problem Löst! ✅

**Fel:**
```
RepositoryNotFoundError: 401 Client Error
Repository Not Found for url: https://huggingface.co/api/models/models/faster-whisper/
LocalEntryNotFoundError: Cannot find an appropriate cached snapshot folder
```

**Orsak:**
`config.yaml` hade fel konfiguration:
```yaml
# FEL:
stt:
  model_path: "models/faster-whisper"  # Detta är inte en giltig modell!
```

Faster Whisper förväntar sig en **modellstorlek** (tiny, base, small, etc.), inte en sökväg.

## Lösning

**Uppdaterade Filer:**

### 1. config/config.yaml
```yaml
# RÄTT:
stt:
  enabled: true
  model_size: "base"  # tiny, base, small, medium, large
  language: "sv"
```

### 2. src/config/settings.py
```python
# Nu används model_size istället för model_path
STT_MODEL_SIZE = os.getenv('STT_MODEL_SIZE') or config.get('stt', {}).get('model_size', 'base')
STT_LANGUAGE = os.getenv('STT_LANGUAGE') or config.get('stt', {}).get('language', 'sv')
```

### 3. src/main.py
```python
# Uppdaterad för att använda model_size
self.stt = FasterWhisper(model_size=STT_MODEL_SIZE, language=STT_LANGUAGE)
```

## Så Här Kör Du Nu

```bash
# 1. Aktivera virtuell miljö
source genio-env/bin/activate

# 2. Verifiera konfiguration
cat config/config.yaml | grep -A 3 "stt:"
# Du bör se:
#   model_size: "base"
#   language: "sv"

# 3. Kör Genio AI (första gången laddar ner modellen)
python src/main.py
```

**Första körningen:**
- Faster Whisper laddar ner `base` modellen (~150 MB)
- Tar 2-5 minuter beroende på internet-hastighet
- Sparas i `~/.cache/huggingface/hub/`
- Nästa gång går det mycket snabbare!

## Modellstorlekar

| Model | Storlek | Hastighet | Kvalitet | För |
|-------|---------|-----------|----------|-----|
| `tiny` | 75 MB | Snabbast | Låg | Raspberry Pi 3, testning |
| `base` | 150 MB | Snabb | Bra | **Raspberry Pi 4/5** ⭐ |
| `small` | 500 MB | Medium | Bättre | Desktop |
| `medium` | 1.5 GB | Långsam | Mycket bra | Server |
| `large` | 3 GB | Långsammas | Bäst | High-end |

## Exempel på Konfigurationer

### Raspberry Pi 4/5 (Standard)
```yaml
stt:
  model_size: "base"  # Perfekt balans
  language: "sv"
```

### Raspberry Pi 3 (Lättare)
```yaml
stt:
  model_size: "tiny"  # Snabbare men lägre kvalitet
  language: "sv"
```

### Desktop/Server (Bättre kvalitet)
```yaml
stt:
  model_size: "small"  # eller "medium"
  language: "sv"
```

## Stödda Språk

Faster Whisper stödjer 99+ språk:
- `sv` - Svenska 🇸🇪
- `en` - Engelska 🇬🇧
- `no` - Norska 🇳🇴
- `da` - Danska 🇩🇰
- `fi` - Finska 🇫🇮
- `de` - Tyska 🇩🇪
- `fr` - Franska 🇫🇷

## Offline Användning

### Ladda ner modell i förväg
```bash
source genio-env/bin/activate
python -c "from faster_whisper import WhisperModel; WhisperModel('base', device='cpu')"
```

Modellen sparas i `~/.cache/huggingface/hub/` och kan användas offline.

## Testning

Skapa `test_stt_quick.py`:
```python
#!/usr/bin/env python3
from src.config.settings import STT_MODEL_SIZE, STT_LANGUAGE

print(f"✓ STT Model: {STT_MODEL_SIZE}")
print(f"✓ Language: {STT_LANGUAGE}")

from src.stt.faster_whisper import FasterWhisper
print("Initializing STT...")
stt = FasterWhisper(model_size=STT_MODEL_SIZE, language=STT_LANGUAGE)
print("✅ STT Ready!")
```

Kör:
```bash
python test_stt_quick.py
```

## Felsökning

### Första nedladdningen tar lång tid
Normal! Modellen är ~150 MB och måste laddas ner en gång.

### "Cannot find cached snapshot"
Kör en gång med internet så modellen laddas ner och cachar.

### Långsam transcription
Använd `tiny` istället för `base`:
```yaml
stt:
  model_size: "tiny"
```

### Dålig kvalitet
Använd större modell (om hårdvaran klarar det):
```yaml
stt:
  model_size: "small"
```

## Mer Information

- **[STT_SETUP.md](STT_SETUP.md)** - Fullständig guide för STT
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Alla felsökningar
- **[README.md](README.md)** - Projektöversikt

---

**Status:** ✅ **FIXAT OCH TESTAT!**

Kör `python src/main.py` för att starta Genio AI!

**Genio AI** 🤖
