# Genio AI - Konfigurationsguide

## Val av konfigurationsmetod

Du kan välja mellan två metoder för att konfigurera Genio AI:

### Metod 1: Endast config.yaml (Enklast) ✅ Rekommenderat

**Fördelar:**
- ✅ En enda fil att redigera
- ✅ Allt samlade på ett ställe
- ✅ Enklare att säkerhetskopiera
- ✅ Ingen .env-fil behövs

**Så här gör du:**

```bash
# Redigera endast config.yaml
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
  model_path: "base"
  language: "sv"

tts:
  enabled: true
  engine: "piper"
  language: "sv"
  voice: "sv_SE-nst-medium"
  model_path: "models/sv_SE-nst-medium.onnx"
  config_path: "models/sv_SE-nst-medium.onnx.json"

mqtt:
  broker: "mqtt://din-broker.com"
  port: 8883
  topic: "genio/agent"
  client_id: "genio_ai"
  username: "ditt_användarnamn"
  password: "ditt_lösenord"

logging:
  level: "INFO"
  file: "logs/genio_ai.log"
```

### Metod 2: .env + config.yaml (Mer flexibelt)

**Fördelar:**
- ✅ Känslig data (API-nycklar, lösenord) i .env
- ✅ .env kan vara git-ignored
- ✅ Bra för team-miljöer
- ✅ Kan override config.yaml-värden

**Så här gör du:**

```bash
# 1. Kopiera exempel-filen
cp .env.example .env

# 2. Redigera .env
nano .env
```

**.env:**
```env
# Känslig data här
PORCUPINE_ACCESS_KEY=din_porcupine_access_key
MQTT_USERNAME=ditt_användarnamn
MQTT_PASSWORD=ditt_lösenord
```

**config.yaml:**
```yaml
# Övrig konfiguration
mqtt:
  broker: "mqtt://din-broker.com"
  port: 8883
  # username och password läses från .env
```

## Prioritetsordning

När både .env och config.yaml finns, används värden i denna ordning:

1. **Miljövariabel från .env** (högst prioritet)
2. **Värde från config.yaml**
3. **Standardvärde i koden** (lägst prioritet)

Exempel:
```
MQTT_PORT definierad i:
.env: 8883          ← Denna används
config.yaml: 1883   ← Ignoreras
kod default: 1883   ← Ignoreras
```

## Minimikonfiguration

**Bara det här MÅSTE konfigureras:**

### I config.yaml (eller .env):

```yaml
wakeword_detection:
  access_key: "din_porcupine_key"  # MÅSTE ha!

mqtt:
  broker: "mqtt://din-broker"     # MÅSTE ha!
  username: "ditt_user"            # MÅSTE ha!
  password: "ditt_pass"            # MÅSTE ha!
```

Allt annat har fungerande standardvärden.

## Rekommenderad konfiguration för olika scenarion

### Scenario 1: Lokal utveckling på en dator

```bash
# Använd .env för hemligheter
cp .env.example .env
nano .env
```

```.env
PORCUPINE_ACCESS_KEY=din_key
MQTT_BROKER=mqtt://localhost
MQTT_PORT=1883
MQTT_USERNAME=admin
MQTT_PASSWORD=password
```

### Scenario 2: Produktion på Raspberry Pi

```bash
# Använd endast config.yaml
nano config/config.yaml
```

Fyll i alla värden i config.yaml, .env behövs inte.

### Scenario 3: Team-utveckling / Git repository

```bash
# 1. Lägg till i .gitignore
echo ".env" >> .gitignore
echo "config/config.yaml" >> .gitignore

# 2. Skapa exempel-filer att commit:a
cp config/config.yaml config/config.yaml.example
cp .env .env.example

# 3. Rensa känslig data från exempel-filerna
nano config/config.yaml.example  # Ta bort riktiga lösenord
nano .env.example                # Ta bort riktiga keys

# 4. Commit endast exempel-filerna
git add .gitignore config/config.yaml.example .env.example
```

## Snabb start - Enklaste sättet

**För de flesta användare:**

1. Öppna config.yaml:
```bash
nano config/config.yaml
```

2. Fyll i dessa tre saker:
```yaml
wakeword_detection:
  access_key: "din_porcupine_key_från_console.picovoice.ai"

mqtt:
  broker: "mqtt://din-broker-adress"
  username: "ditt_mqtt_användarnamn"
  password: "ditt_mqtt_lösenord"
```

3. Klart! Ingen .env-fil behövs.

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

### Måste jag ha en .env-fil?
**Nej!** Du kan lägga allt i config.yaml. .env är valfritt.

### Vilken är enklast?
**config.yaml** - bara en fil att redigera.

### Vilken är säkrast?
**.env** - kan enkelt exkluderas från git och backuper.

### Kan jag använda båda?
**Ja!** .env-värden har företräde över config.yaml.

### Vad händer om en inställning saknas?
Standardvärden används. Vissa (som PORCUPINE_ACCESS_KEY) ger en varning.

### Hur ändrar jag konfiguration efter installation?
Redigera bara config.yaml (eller .env) och starta om applikationen.

---

**Rekommendation:** Använd **endast config.yaml** om du inte har speciella behov.

**Genio AI** 🤖
