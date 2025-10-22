# Genio AI - Installationsguide

## Systemkrav
- Raspberry Pi 4 eller 5
- Raspberry Pi OS (Bookworm eller senare)
- Python 3.8+
- Minst 2GB RAM
- Internetanslutning för initial installation

## Installation

### Problem med "externally-managed-environment"

Om du får felet `error: externally-managed-environment` när du försöker installera requirements.txt, beror det på att moderna Python-installationer skyddar systemets Python-miljö.

**Rekommenderad lösning: Använd virtuell miljö (venv)**

### Metod 1: Virtuell Miljö (Rekommenderat) ✅

```bash
# 1. Klona repository
git clone https://github.com/fredrik-svg/genio.git
cd genio/raspberry-pi-voice-agent

# 2. Skapa virtuell miljö
python3 -m venv genio-env

# 3. Aktivera virtuell miljö
source genio-env/bin/activate

# 4. Uppgradera pip
pip install --upgrade pip

# 5. Installera dependencies
pip install -r requirements.txt

# 6. Installera Piper TTS
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
tar -xzf piper_arm64.tar.gz
sudo mv piper/piper /usr/local/bin/
sudo chmod +x /usr/local/bin/piper

# 7. Ladda ner svensk röstmodell
mkdir -p models
cd models
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json
cd ..

# 8. Konfigurera applikationen
nano config/config.yaml  # Redigera med dina inställningar

# 9. Testa installation
python test_piper.py

# 10. Kör Genio AI
python src/main.py
```

### Metod 2: Använd pipx (För systeminstallationer)

```bash
# Installera pipx
sudo apt install pipx
pipx ensurepath

# Skapa virtuell miljö och installera
cd genio/raspberry-pi-voice-agent
python3 -m venv genio-env
source genio-env/bin/activate
pip install -r requirements.txt
```

### Metod 3: Använd --break-system-packages (INTE REKOMMENDERAT) ⚠️

```bash
# Endast om du vet vad du gör!
pip install -r requirements.txt --break-system-packages
```

**Varning:** Detta kan orsaka konflikter med systempaket.

### Metod 4: Använd UV (Modern pakethanterare)

```bash
# Installera uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Skapa och aktivera miljö
uv venv
source .venv/bin/activate

# Installera dependencies
uv pip install -r requirements.txt
```

## Automatisk aktivering av virtuell miljö

### Skapa aktiveringsscript

Skapa `activate.sh`:

```bash
#!/bin/bash
# Genio AI - Activation Script

echo "🤖 Aktiverar Genio AI miljö..."

# Gå till projektmapp
cd "$(dirname "$0")"

# Aktivera virtuell miljö
if [ -d "genio-env" ]; then
    source genio-env/bin/activate
    echo "✅ Virtuell miljö aktiverad!"
    echo "📍 Python: $(which python)"
    echo "📦 Pip: $(which pip)"
else
    echo "❌ Virtuell miljö hittades inte!"
    echo "Kör: python3 -m venv genio-env"
    exit 1
fi
```

Gör den körbar:
```bash
chmod +x activate.sh
```

Använd den:
```bash
source activate.sh
```

## Systemd Service (Autostart)

För att köra Genio AI som en systemtjänst:

### 1. Skapa service-fil

```bash
sudo nano /etc/systemd/system/genio-ai.service
```

Innehåll:
```ini
[Unit]
Description=Genio AI Voice Assistant
After=network.target sound.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/genio/raspberry-pi-voice-agent
Environment="PATH=/home/pi/genio/raspberry-pi-voice-agent/genio-env/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/pi/genio/raspberry-pi-voice-agent/genio-env/bin/python src/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Aktivera och starta tjänsten

```bash
# Ladda om systemd
sudo systemctl daemon-reload

# Aktivera tjänsten (autostart)
sudo systemctl enable genio-ai

# Starta tjänsten
sudo systemctl start genio-ai

# Kontrollera status
sudo systemctl status genio-ai

# Se loggar
sudo journalctl -u genio-ai -f
```

## Felsökning

### Problem: "No module named 'paho'"

**Lösning:**
```bash
source genio-env/bin/activate
pip install paho-mqtt
```

### Problem: "Porcupine access key required"

**Lösning:** Du behöver en API-nyckel från Picovoice:
1. Gå till https://console.picovoice.ai/
2. Skapa ett konto
3. Generera en Access Key
4. Uppdatera din kod med nyckeln

### Problem: MQTT connection failed

**Lösning:**
1. Kontrollera att MQTT-broker är igång
2. Verifiera port (nu 8883 för SSL/TLS)
3. Kontrollera username/password i config.yaml

```bash
# Testa MQTT-anslutning
mosquitto_pub -h your_broker -p 8883 -t test -m "hello" -u username -P password
```

### Problem: Audio device not found

**Lösning:**
```bash
# Lista ljudenheter
aplay -l
arecord -l

# Installera ALSA-verktyg om de saknas
sudo apt install alsa-utils

# Konfigurera standardenhet
sudo nano /etc/asound.conf
```

## MQTT Konfiguration (Port 8883)

Port 8883 används för MQTT över TLS/SSL. Se till att din broker stödjer detta.

### Mosquitto TLS Setup

```bash
# Installera mosquitto
sudo apt install mosquitto mosquitto-clients

# Konfigurera TLS
sudo nano /etc/mosquitto/mosquitto.conf
```

Lägg till:
```conf
listener 8883
cafile /etc/mosquitto/ca_certificates/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
```

Om du vill använda port 8883 utan TLS (ej rekommenderat):
```conf
listener 8883
allow_anonymous true
```

## Nästa steg

1. ✅ Installera dependencies i virtuell miljö
2. ✅ Konfigurera MQTT (port 8883)
3. ✅ Ladda ner Piper-modeller
4. ✅ Testa med `test_piper.py`
5. ✅ Konfigurera `config/config.yaml`
6. ✅ Kör `python src/main.py`

## Support

För mer hjälp, se:
- `README.md` - Projektöversikt
- `PIPER_INSTALLATION.md` - Piper TTS guide
- `REBRANDING.md` - Om Genio AI

---

**Genio AI** 🤖 - Din intelligenta röstassistent
