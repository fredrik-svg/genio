# Genio AI - Konfigurationsguide

## Konfiguration med config.yaml

Genio AI konfigureras genom en enda YAML-fil: `config/config.yaml`

**Fördelar:**
- ✅ En enda fil att redigera
- ✅ Allt samlat på ett ställe
- ✅ Enklare att säkerhetskopiera
- ✅ Tydlig struktur med kommentarer

**Så här gör du:**

```bash
# Redigera config.yaml
nano config/config.yaml
```

```yaml
wakeword_detection:
  enabled: true
  access_key: "din_porcupine_access_key"  # Lägg till din key här
  keyword: "porcupine"
  sensitivity: 0.5

stt:
  enabled: true
  model_size: "base"
  language: "sv"

tts:
  enabled: true
  engine: "piper"
  language: "sv"
  voice: "sv_SE-nst-medium"
  model_path: "models/sv_SE-nst-medium.onnx"
  config_path: "models/sv_SE-nst-medium.onnx.json"

mqtt:
  broker: "din-broker.com"
  port: 8883
  topic: "genio/agent"
  client_id: "genio_ai"
  username: "ditt_användarnamn"
  password: "ditt_lösenord"
  use_tls: true

logging:
  level: "INFO"
  file: "logs/genio_ai.log"
```

## Minimikonfiguration

**Bara det här MÅSTE konfigureras:**

```yaml
wakeword_detection:
  access_key: "din_porcupine_key"  # MÅSTE ha!

mqtt:
  broker: "din-broker"     # MÅSTE ha!
  username: "ditt_user"    # MÅSTE ha!
  password: "ditt_pass"    # MÅSTE ha!
```

Allt annat har fungerande standardvärden.

## Rekommenderad konfiguration

### Produktion på Raspberry Pi eller lokal utveckling

```bash
# Redigera config.yaml
nano config/config.yaml
```

Fyll i alla nödvändiga värden i config.yaml.

### Team-utveckling / Git repository

För att undvika att dela känsliga credentials:

```bash
# 1. Lägg till i .gitignore
echo "config/config.yaml" >> .gitignore

# 2. Skapa exempel-fil att commit:a
cp config/config.yaml config/config.yaml.example

# 3. Rensa känslig data från exempel-filen
nano config/config.yaml.example  # Ta bort riktiga lösenord och nycklar

# 4. Commit endast exempel-filen
git add .gitignore config/config.yaml.example
```

## Snabbstart

**För de flesta användare:**

1. Öppna config.yaml:
```bash
nano config/config.yaml
```

2. Fyll i dessa fyra saker (MÅSTE ÄNDRAS från placeholder-värden):
```yaml
wakeword_detection:
  access_key: "din_porcupine_key_från_console.picovoice.ai"  # Ändra från YOUR_PORCUPINE_ACCESS_KEY_HERE

mqtt:
  broker: "din-broker-adress"  # Ändra från YOUR_MQTT_BROKER_ADDRESS
  username: "ditt_mqtt_användarnamn"  # Ändra från YOUR_MQTT_USERNAME
  password: "ditt_mqtt_lösenord"  # Ändra från YOUR_MQTT_PASSWORD
```

3. Klart! Du är redo att köra Genio AI.

## Validera din konfiguration

Kör detta för att se vilka värden som används:

```bash
source genio-env/bin/activate
python -c "
from src.config import settings
print('Porcupine Key:', 'Konfigurerad ✓' if settings.PORCUPINE_ACCESS_KEY else 'SAKNAS ✗')
print('MQTT Broker:', settings.MQTT_BROKER)
print('MQTT Port:', settings.MQTT_PORT)
print('Wake Word:', settings.WAKE_WORD)
print('TTS Model:', settings.TTS_MODEL_PATH)
"
```

## Vanliga frågor

### Var lagrar jag känslig data?
Alla konfigurationsvärden, inklusive känslig data som API-nycklar och lösenord, lagras i `config/config.yaml`. Se till att inte dela denna fil publikt eller committa den med riktiga credentials till Git.

### Vad händer om en inställning saknas?
Standardvärden används. Vissa viktiga inställningar (som PORCUPINE_ACCESS_KEY, MQTT_BROKER, MQTT_USERNAME, MQTT_PASSWORD) ger en varning om de har placeholder-värden eller saknas.

### Hur ändrar jag konfiguration efter installation?
Redigera bara config.yaml och starta om applikationen.

---

**Genio AI** 🤖
