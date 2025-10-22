# Genio AI - Snabbreferens

## Installation (En rad)

```bash
git clone https://github.com/fredrik-svg/genio.git && cd genio/raspberry-pi-voice-agent && chmod +x install.sh && ./install.sh
```

**Efter installation:**
```bash
# 1. Skaffa Porcupine Access Key från https://console.picovoice.ai/
# 2. Redigera config.yaml och lägg till din key
nano config/config.yaml

# 3. Testa wake word
source genio-env/bin/activate
python test_wakeword.py
```

## Daglig användning

```bash
# Aktivera miljö
cd genio/raspberry-pi-voice-agent
source genio-env/bin/activate

# Starta Genio AI
python src/main.py

# Deaktivera miljö när du är klar
deactivate
```

## Vanliga kommandon

### Starta Genio AI
```bash
source genio-env/bin/activate
python src/main.py
```

### Testa TTS
```bash
source genio-env/bin/activate
python test_piper.py
```

### Visa loggar
```bash
tail -f logs/genio_ai.log
```

### Uppdatera konfiguration
```bash
nano config/config.yaml
```

### Installera nya paket
```bash
source genio-env/bin/activate
pip install <paket-namn>
```

## Systemd Service (Autostart)

### Skapa service
```bash
sudo nano /etc/systemd/system/genio-ai.service
```

```ini
[Unit]
Description=Genio AI Voice Assistant
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/genio/raspberry-pi-voice-agent
Environment="PATH=/home/pi/genio/raspberry-pi-voice-agent/genio-env/bin"
ExecStart=/home/pi/genio/raspberry-pi-voice-agent/genio-env/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Hantera service
```bash
sudo systemctl enable genio-ai   # Aktivera autostart
sudo systemctl start genio-ai    # Starta
sudo systemctl stop genio-ai     # Stoppa
sudo systemctl restart genio-ai  # Starta om
sudo systemctl status genio-ai   # Visa status
sudo journalctl -u genio-ai -f   # Visa loggar
```

## MQTT Konfiguration

### Port 8883 (TLS/SSL)
```yaml
mqtt:
  broker: "mqtt://your-broker.com"
  port: 8883
  username: "your_username"
  password: "your_password"
```

### Testa MQTT-anslutning
```bash
# Installera mosquitto-clients
sudo apt install mosquitto-clients

# Testa publicering
mosquitto_pub -h your-broker.com -p 8883 -t "genio/test" -m "hello" -u username -P password

# Lyssna på topic
mosquitto_sub -h your-broker.com -p 8883 -t "genio/#" -u username -P password
```

## Felsökning

### Problem: externally-managed-environment
```bash
# Skapa virtuell miljö
python3 -m venv genio-env
source genio-env/bin/activate
pip install -r requirements.txt
```

### Problem: Piper hittas inte
```bash
# Kontrollera installation
which piper
piper --version

# Ominstallera
sudo rm /usr/local/bin/piper
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
tar -xzf piper_arm64.tar.gz
sudo mv piper/piper /usr/local/bin/
sudo chmod +x /usr/local/bin/piper
```

### Problem: MQTT ansluter inte
```bash
# Kontrollera broker är igång
ping your-broker.com

# Testa port
telnet your-broker.com 8883

# Kontrollera config
cat config/config.yaml | grep mqtt -A 6
```

### Problem: Ingen ljud
```bash
# Lista ljudenheter
aplay -l
arecord -l

# Testa uppspelning
speaker-test -t wav -c 2

# Installera ALSA
sudo apt install alsa-utils
```

### Problem: ModuleNotFoundError
```bash
# Aktivera virtuell miljö först!
source genio-env/bin/activate

# Installera saknat paket
pip install <paket-namn>
```

## Konfigurationsfiler

- `config/config.yaml` - Huvudkonfiguration
- `src/config/settings.py` - Python-inställningar
- `logs/genio_ai.log` - Applikationsloggar

## Viktiga sökvägar

- **Projekt:** `~/genio/raspberry-pi-voice-agent/`
- **Virtuell miljö:** `~/genio/raspberry-pi-voice-agent/genio-env/`
- **Modeller:** `~/genio/raspberry-pi-voice-agent/models/`
- **Loggar:** `~/genio/raspberry-pi-voice-agent/logs/`
- **Piper binary:** `/usr/local/bin/piper`

## Uppdatera Genio AI

```bash
cd genio/raspberry-pi-voice-agent
git pull origin main
source genio-env/bin/activate
pip install -r requirements.txt --upgrade
```

## Prestanda

### Minska CPU-användning
- Använd `low` kvalitet röstmodell istället för `medium`
- Öka wake word sensitivity threshold
- Minska MQTT polling-frekvens

### Förbättra ljudkvalitet
- Använd `high` kvalitet röstmodell
- Öka sample rate i audio-konfiguration
- Använd extern USB-ljudkort

## Säkerhet

### MQTT över TLS
```bash
# Generera certifikat för Mosquitto
sudo mosquitto_passwd -c /etc/mosquitto/passwd username

# Konfigurera TLS i mosquitto.conf
listener 8883
cafile /etc/mosquitto/ca_certificates/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key
```

### Skydda konfiguration
```bash
# Sätt rätt rättigheter
chmod 600 config/config.yaml
```

## Backup

```bash
# Backup konfiguration
tar -czf genio-ai-backup-$(date +%Y%m%d).tar.gz config/ models/

# Restore
tar -xzf genio-ai-backup-20251022.tar.gz
```

---

**Genio AI** 🤖 - Din intelligenta röstassistent
