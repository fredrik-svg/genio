# Genio AI - Lösning för Installation

## Problem: "Porcupine" paket hittades inte

### Orsak
`Porcupine` är inte namnet på pip-paketet. Det riktiga paketet heter `pvporcupine`.

### Lösning ✅
Vi har uppdaterat `requirements.txt` till:
```
pvporcupine
pyaudio
faster-whisper
paho-mqtt
sounddevice
numpy
piper-tts
PyYAML
python-dotenv
```

## Fullständig Installation

### Steg 1: Klona och kör installationsscript

```bash
git clone https://github.com/fredrik-svg/genio.git
cd genio/raspberry-pi-voice-agent
chmod +x install.sh
./install.sh
```

Scriptet kommer att:
- ✅ Skapa virtuell miljö (genio-env)
- ✅ Installera systempaket för PyAudio
- ✅ Installera alla Python-dependencies
- ✅ Ladda ner Piper TTS
- ✅ Ladda ner svensk röstmodell
- ✅ Skapa .env fil

### Steg 2: Skaffa Porcupine Access Key

1. Gå till [Picovoice Console](https://console.picovoice.ai/)
2. Skapa ett gratis konto
3. Gå till "Access Keys"
4. Klicka "Create Access Key"
5. Kopiera din access key

### Steg 3: Konfigurera .env

```bash
nano .env
```

Uppdatera:
```env
# VIKTIGT!
PORCUPINE_ACCESS_KEY=din_access_key_här

# MQTT (optional - kan också konfigureras i config.yaml)
MQTT_BROKER=mqtt://din-broker.com
MQTT_PORT=8883
MQTT_USERNAME=ditt_användarnamn
MQTT_PASSWORD=ditt_lösenord
```

### Steg 4: Konfigurera MQTT

```bash
nano config/config.yaml
```

Uppdatera MQTT-sektionen:
```yaml
mqtt:
  broker: "mqtt://din-broker.com"
  port: 8883
  topic: "genio/agent"
  client_id: "genio_ai"
  username: "ditt_användarnamn"
  password: "ditt_lösenord"
```

### Steg 5: Testa installationen

```bash
# Aktivera virtuell miljö
source genio-env/bin/activate

# Testa wake word detection
python test_wakeword.py
# Säg "porcupine" när den lyssnar

# Testa TTS
python test_piper.py
# Du bör höra en svensk röst
```

### Steg 6: Kör Genio AI

```bash
source genio-env/bin/activate
python src/main.py
```

## Vanliga Problem och Lösningar

### Problem 1: PyAudio installation error

**Symptom:**
```
error: portaudio.h: No such file or directory
```

**Lösning:**
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
source genio-env/bin/activate
pip install pyaudio
```

### Problem 2: "Invalid Porcupine Access Key"

**Symptom:**
```
pvporcupine.PorcupineInvalidArgumentError: Invalid access key
```

**Lösning:**
1. Verifiera att du har kopierat hela access key (ingen extra mellanslag)
2. Kontrollera att .env filen laddas: `cat .env | grep PORCUPINE`
3. Testa direkt: `python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('PORCUPINE_ACCESS_KEY'))"`

### Problem 3: "No module named 'dotenv'"

**Symptom:**
```
ModuleNotFoundError: No module named 'dotenv'
```

**Lösning:**
```bash
source genio-env/bin/activate
pip install python-dotenv
```

### Problem 4: ALSA errors eller ingen ljud

**Symptom:**
```
ALSA lib pcm.c:... snd_pcm_open... No such file or directory
```

**Lösning:**
```bash
# Installera ALSA-verktyg
sudo apt-get install alsa-utils

# Lista ljudenheter
aplay -l
arecord -l

# Testa mikrofon
arecord -d 5 test.wav
aplay test.wav

# Konfigurera standardenhet om nödvändigt
sudo nano /etc/asound.conf
```

### Problem 5: Faster-Whisper installation error

**Symptom:**
```
ERROR: Could not build wheels for faster-whisper
```

**Lösning:**
```bash
# Installera build-dependencies
sudo apt-get install build-essential

# För Raspberry Pi, använd lätt version
source genio-env/bin/activate
pip install faster-whisper --no-build-isolation
```

### Problem 6: MQTT ansluter inte

**Symptom:**
```
Connection refused [Errno 111]
```

**Lösning:**
```bash
# Kontrollera att broker är igång
ping din-broker.com

# Testa port
telnet din-broker.com 8883

# För lokal Mosquitto
sudo systemctl status mosquitto
sudo systemctl start mosquitto

# Testa anslutning
mosquitto_pub -h localhost -p 8883 -t test -m "hello" -u user -P pass
```

## Wake Word Alternativ

### Inbyggda wake words (gratis med Porcupine):
- `porcupine` (standard i Genio AI)
- `alexa`
- `computer`
- `jarvis`
- `hey google`
- `hey siri`

### Ändra wake word:

I `.env`:
```env
WAKE_WORD=computer
```

Eller i `config/config.yaml`:
```yaml
wakeword_detection:
  keyword: "computer"
```

### Custom wake word:
Du kan träna egna wake words via [Picovoice Console](https://console.picovoice.ai/) och ladda ner .ppn-filen.

## MQTT Port 8883 (TLS/SSL)

Port 8883 används för säker MQTT över TLS/SSL.

### För Mosquitto med TLS:

```bash
# Installera Mosquitto
sudo apt-get install mosquitto mosquitto-clients

# Konfigurera TLS
sudo nano /etc/mosquitto/mosquitto.conf
```

Lägg till:
```conf
listener 8883
cafile /etc/mosquitto/ca_certificates/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
allow_anonymous false
password_file /etc/mosquitto/passwd
```

### För testning utan TLS (ej rekommenderat):

Använd port 1883 istället:
```env
MQTT_PORT=1883
```

## Dokumentation

- 📖 [README.md](README.md) - Projektöversikt
- 🚀 [QUICKREF.md](QUICKREF.md) - Snabbreferens
- 🔧 [INSTALLATION.md](INSTALLATION.md) - Detaljerad installation
- 🎤 [WAKEWORD_SETUP.md](WAKEWORD_SETUP.md) - Wake word konfiguration
- 🎨 [PIPER_INSTALLATION.md](PIPER_INSTALLATION.md) - Piper TTS guide

## Support

Om du fortsätter ha problem:
1. Kontrollera att du kör från virtuell miljö: `which python`
2. Verifiera dependencies: `pip list`
3. Kontrollera loggar: `tail -f logs/genio_ai.log`
4. Kör tester:
   - `python test_wakeword.py`
   - `python test_piper.py`

---

**Genio AI** 🤖 - Din intelligenta röstassistent
