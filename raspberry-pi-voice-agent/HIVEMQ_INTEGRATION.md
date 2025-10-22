# HiveMQ Integration - Ändringssammanfattning

**Datum:** 2025-10-22

## Översikt

Genio AI är nu konfigurerad för att kommunicera med HiveMQ Cloud på adressen:
- **Broker:** `7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud`
- **Port:** `8883` (TLS/SSL)
- **Region:** EU (Frankfurt)

## Ändringar

### 1. `config/config.yaml` ✅
**Uppdaterat:**
- MQTT broker-adress till HiveMQ Cloud
- Lagt till `use_tls: true` för säker anslutning
- Förtydligade kommentarer för HiveMQ

```yaml
mqtt:
  broker: "7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud"
  port: 8883
  username: ""  # Din HiveMQ username
  password: ""  # Din HiveMQ password
  use_tls: true
```

### 2. `src/config/settings.py` ✅
**Lagt till:**
- `MQTT_USE_TLS` inställning för TLS/SSL-stöd
- Läser från både environment variables och config.yaml

```python
MQTT_USE_TLS = os.getenv('MQTT_USE_TLS', 'true').lower() == 'true' if os.getenv('MQTT_USE_TLS') else config.get('mqtt', {}).get('use_tls', True)
```

### 3. `src/main.py` ✅
**Uppdaterat:**
- Importerat `ssl` för TLS-stöd
- Lagt till `MQTT_USE_TLS` i imports
- Implementerat TLS/SSL-konfiguration i `setup_mqtt()`

```python
if MQTT_USE_TLS:
    self.logger.info("Enabling TLS/SSL for secure connection...")
    self.mqtt_client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
    self.mqtt_client.tls_insecure_set(False)
```

### 4. `test_mqtt.py` ✅ (Nytt)
**Skapat komplett testskript:**
- Testar anslutning till HiveMQ Cloud
- Verifierar TLS/SSL-konfiguration
- Testar publish/subscribe funktionalitet
- Ger tydlig feedback och felsökning

**Användning:**
```bash
source genio-env/bin/activate
python test_mqtt.py
```

**Förväntat resultat:**
```
✅ MQTT Connection Successful!
📤 Publishing test message...
📥 Message Received!
🎉 All tests passed!
```

### 5. Konfigurationsfiler uppdaterade ✅
**Uppdaterat:**
- HiveMQ Cloud broker-adress i config.yaml
- Lagt till `use_tls: true`
- Förtydligade kommentarer

### 6. `HIVEMQ_SETUP.md` ✅ (Nytt)
**Skapat omfattande guide:**
- Snabbstart för HiveMQ-konfiguration
- Credentials-hantering
- MQTT topics-struktur
- Säkerhetsguide (TLS/SSL)
- Troubleshooting
- n8n integration-exempel
- Testing scenarios
- Performance tips

### 7. `README.md` ✅
**Uppdaterat:**
- Lagt till länk till HIVEMQ_SETUP.md
- Uppdaterat MQTT troubleshooting-sektion
- Referens till `test_mqtt.py`

## Nya Funktioner

### TLS/SSL Säkerhet
- ✅ Automatisk TLS v1.2 konfiguration
- ✅ Certificate verification enabled
- ✅ Säker kommunikation med HiveMQ Cloud

### MQTT Test Script
- ✅ Komplett connection test
- ✅ Publish/Subscribe verification
- ✅ Detaljerad feldiagnostik
- ✅ Användarvänlig output

### Förbättrad Felhantering
- ✅ Graceful fallback om MQTT misslyckas
- ✅ Tydliga felmeddelanden
- ✅ Logging för debugging

## Konfiguration

### Minimikonfiguration

**config/config.yaml:**
```yaml
wakeword_detection:
  access_key: "DIN_PORCUPINE_KEY"

mqtt:
  broker: "7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud"
  port: 8883
  username: "ditt_hivemq_användarnamn"
  password: "ditt_hivemq_lösenord"
  use_tls: true
```

## Testing

### Steg 1: Konfigurera Credentials
```bash
nano config/config.yaml
# Lägg till HiveMQ username och password
```

### Steg 2: Testa Anslutningen
```bash
source genio-env/bin/activate
python test_mqtt.py
```

### Steg 3: Kör Genio AI
```bash
python src/main.py
```

## MQTT Topics

Genio AI använder dessa topics:

| Topic | Beskrivning | Riktning |
|-------|-------------|----------|
| `genio/commands` | Röstkommandon | Genio → n8n |
| `genio/responses` | Svar från n8n | n8n → Genio |
| `genio/status` | Status updates | Genio → n8n |
| `genio/test` | Test messages | Both |

## n8n Integration

### MQTT Trigger Node (n8n)
```json
{
  "protocol": "mqtts",
  "host": "7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud",
  "port": 8883,
  "username": "ditt_hivemq_användarnamn",
  "password": "ditt_hivemq_lösenord",
  "topic": "genio/commands"
}
```

### Workflow
```
Genio AI Wake Word → Lyssna → Transkribera 
  ↓
MQTT Publish (genio/commands)
  ↓
n8n MQTT Trigger → Bearbeta → AI/API
  ↓
n8n MQTT Out (genio/responses)
  ↓
Genio AI Subscribe → TTS → Tala
```

## Troubleshooting

### Problem: "Connection refused - bad username or password"
**Lösning:**
1. Verifiera credentials i config/config.yaml
2. Kontrollera HiveMQ Console att användaren finns
3. Kör `python test_mqtt.py` för att testa

### Problem: "Network unreachable"
**Lösning:**
```bash
# Testa nätverksanslutning
ping 7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud

# Testa port
nc -zv 7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud 8883
```

### Problem: "Certificate verification failed"
**Lösning:**
```bash
sudo apt-get update
sudo apt-get install ca-certificates
source genio-env/bin/activate
pip install --upgrade certifi
```

## Säkerhet

### Best Practices
1. ✅ Lagra credentials i config.yaml (ej i Git)
2. ✅ Starka lösenord (12+ tecken)
3. ✅ TLS/SSL alltid aktiverat
4. ✅ Unika användare per enhet
5. ❌ Commita ALDRIG credentials

### TLS Configuration
```python
# Automatiskt konfigurerat i main.py
client.tls_set(
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLSv1_2
)
```

## Dokumentation

📖 **Nya guider:**
- [HIVEMQ_SETUP.md](HIVEMQ_SETUP.md) - Komplett HiveMQ-guide
- test_mqtt.py - MQTT connection test

📖 **Uppdaterade:**
- README.md - HiveMQ-referenser
- config.yaml - HiveMQ-konfiguration

## Status

✅ **Klar för användning**

**Nästa steg:**
1. Konfigurera HiveMQ credentials i `config/config.yaml`
2. Kör `python test_mqtt.py` för att testa anslutningen
3. Konfigurera n8n MQTT nodes
4. Kör `python src/main.py`

---

**Genio AI** 🤖 × **HiveMQ Cloud** ☁️

Säker, skalbar MQTT-kommunikation för röstassistent-integration med n8n.
