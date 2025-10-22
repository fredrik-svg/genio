# Genio AI - Senaste Fixar och Uppdateringar

## 🔧 Problem Lösta (22 Oktober 2025)

### 1. ImportError: cannot import name 'FasterWhisper' ✅

**Problem:**
```python
ImportError: cannot import name 'FasterWhisper' from 'stt.faster_whisper'
```

**Orsak:**
Klassen hette `FasterWhisperSTT` men koden försökte importera `FasterWhisper`.

**Lösning:**
Lade till alias i `src/stt/faster_whisper.py`:
```python
# Alias för backward compatibility
FasterWhisper = FasterWhisperSTT
```

**Status:** ✅ Fixat

---

### 2. Konfiguration förtydligad ✅

**Fråga:**
"Hur konfigurerar jag Genio AI?"

**Svar:**
Använd `config.yaml`:

```yaml
# config/config.yaml
wakeword_detection:
  access_key: "din_porcupine_key"

mqtt:
  broker: "mqtt://din-broker.com"
  username: "ditt_user"
  password: "ditt_pass"
```

**Fördelar:**
- ✅ En fil att hantera
- ✅ Enkelt att säkerhetskopiera
- ✅ Inga extra beroenden

**Dokumentation:**
Se [CONFIG_GUIDE.md](CONFIG_GUIDE.md)

**Status:** ✅ Förtydligat med guide

---

### 3. Porcupine access key konfiguration förbättrad ✅

**Förbättringar:**

1. **Lagt till i config.yaml:**
```yaml
wakeword_detection:
  access_key: ""  # Lägg till här
  keyword: "porcupine"
```

2. **Bättre felmeddelande:**
När access key saknas:
```
⚠️  VARNING: PORCUPINE_ACCESS_KEY är inte konfigurerad!
   Lägg till i config.yaml
   Skaffa gratis key: https://console.picovoice.ai/
```

**Status:** ✅ Förbättrat

---

## 📝 Nya Dokumentationsfiler

### CONFIG_GUIDE.md
Komplett guide om:
- Konfiguration med config.yaml
- Minimikonfiguration
- Scenarion (utveckling vs produktion)
- Snabbstart

### Uppdaterade README.md
- Klarare installationsinstruktioner
- Två tydliga konfigurationsmetoder
- Länk till CONFIG_GUIDE.md

### Uppdaterade TROUBLESHOOTING.md
- Lösning för ImportError
- Snabba fixar

---

## 🚀 Så här installerar du nu (Uppdaterat)

```bash
# 1. Klona och installera
git clone https://github.com/fredrik-svg/genio.git
cd genio/raspberry-pi-voice-agent
chmod +x install.sh
./install.sh

# 2. Konfigurera config.yaml
nano config/config.yaml
# Fyll i access_key, mqtt-inställningar

# 3. Skaffa Porcupine Access Key
# Gå till: https://console.picovoice.ai/
# Skapa konto och generera gratis key

# 4. Testa
source genio-env/bin/activate
python test_wakeword.py   # Säg "porcupine"
python test_piper.py       # Hör svensk röst

# 5. Kör Genio AI
python src/main.py
```

---

## 📦 Uppdaterade Filer

### Kodfixar:
- ✅ `src/stt/faster_whisper.py` - Lagt till FasterWhisper alias
- ✅ `src/config/settings.py` - Bättre felmeddelanden
- ✅ `config/config.yaml` - Lagt till access_key fält

### Nya/uppdaterade guider:
- ✅ `CONFIG_GUIDE.md` - NY! Komplett konfigurationsguide
- ✅ `README.md` - Uppdaterad med tydligare instruktioner
- ✅ `TROUBLESHOOTING.md` - Nya lösningar
- ✅ `install.sh` - Förbättrade instruktioner

---

## ✅ Checklista för ny installation

- [ ] Klonat repository
- [ ] Kört `./install.sh`
- [ ] Skaffat Porcupine Access Key från https://console.picovoice.ai/
- [ ] Konfigurerat config.yaml
- [ ] Testat wake word: `python test_wakeword.py`
- [ ] Testat TTS: `python test_piper.py`
- [ ] Konfigurerat MQTT-broker-inställningar
- [ ] Kört `python src/main.py`

---

## 🆘 Hjälp och Support

**Problem med installation?**
1. Läs [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Läs [CONFIG_GUIDE.md](CONFIG_GUIDE.md)
3. Kontrollera att virtuell miljö är aktiverad: `which python`

**Vanligaste felen:**
1. ❌ Glömt aktivera virtuell miljö → `source genio-env/bin/activate`
2. ❌ Ingen Porcupine key → Lägg till i config.yaml
3. ❌ MQTT-anslutning misslyckas → Kontrollera broker, port, credentials

---

**Senast uppdaterad:** 22 Oktober 2025

**Genio AI** 🤖 - Din intelligenta röstassistent
