# HiveMQ Cloud Setup Guide - Genio AI

## Overview

Genio AI är nu konfigurerad att kommunicera med HiveMQ Cloud för MQTT-meddelanden till och från n8n.

**HiveMQ Cloud Broker:**
- **Adress:** `7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud`
- **Port:** `8883` (TLS/SSL)
- **Region:** EU (Frankfurt)

## Snabbstart

### 1. Konfigurera HiveMQ Credentials

**Alternativ A: Använd config.yaml (Enklast)**

```bash
nano config/config.yaml
```

Uppdatera MQTT-sektionen:
```yaml
mqtt:
  broker: "7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud"
  port: 8883
  username: "ditt_hivemq_användarnamn"  # Från HiveMQ Console
  password: "ditt_hivemq_lösenord"       # Från HiveMQ Console
  use_tls: true
```

### 2. Testa HiveMQ-anslutningen

```bash
source genio-env/bin/activate
python test_mqtt.py
```

**Förväntat resultat:**
```
✅ MQTT Connection Successful!
   Connected to: 7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud:8883

📤 Publishing test message...
✅ Message published successfully

📥 Message Received!
   Payload: Genio AI Test Message

✅ Test message successfully received!

🎉 All tests passed! HiveMQ connection is working perfectly.
```

### 3. Kör Genio AI

```bash
source genio-env/bin/activate
python src/main.py
```

## HiveMQ Cloud Console

### Skaffa Credentials

1. Gå till [HiveMQ Cloud Console](https://console.hivemq.cloud/)
2. Logga in på ditt konto
3. Välj din cluster: `7dab69000883410aba47967fb078d6d9`
4. Gå till **Access Management**
5. Skapa eller kopiera användare och lösenord

### Övervaka MQTT-trafik

I HiveMQ Console kan du:
- Se aktiva anslutningar
- Övervaka meddelanden i realtid
- Kontrollera topics och subscriptions
- Granska logs och metrics

**Web Client (live monitoring):**
1. Gå till **Web Client** i HiveMQ Console
2. Connect med dina credentials
3. Subscribe till `genio/#` för att se alla Genio AI-meddelanden

## MQTT Topics

Genio AI använder följande topics:

### Standardtopics

| Topic | Beskrivning | Riktning |
|-------|-------------|----------|
| `genio/agent` | Huvudtopic för agent | Base |
| `genio/commands` | Röstkommandon från Genio | Publish (Genio → n8n) |
| `genio/responses` | Svar från n8n | Subscribe (n8n → Genio) |
| `genio/status` | Status-updates | Publish (Genio → n8n) |
| `genio/test` | Test-meddelanden | Both |

### Anpassa Topics

Ändra i `config/config.yaml`:
```yaml
mqtt:
  topic: "genio/agent"  # Bas-topic, andra topics byggs från denna
```

## Säkerhet

### TLS/SSL

HiveMQ Cloud **kräver** TLS/SSL-kryptering:

```yaml
mqtt:
  port: 8883        # Port för TLS
  use_tls: true     # Måste vara true
```

Genio AI använder:
- **Protocol:** TLS v1.2
- **Certificate Verification:** Enabled
- **Certificate Authority:** System CA certificates

### Credentials

**Bästa praxis:**
1. ✅ Lagra credentials i `config/config.yaml` (läggs till `.gitignore`)
2. ✅ Skapa unika användare för varje Genio AI-enhet
3. ✅ Använd starka lösenord (minst 12 tecken)
4. ❌ Commita ALDRIG credentials till Git

## Troubleshooting

### Problem: "Connection refused - bad username or password"

**Lösning:**
```bash
# Verifiera credentials i config
cat config/config.yaml | grep -A 5 mqtt

# Testa anslutningen
python test_mqtt.py
```

### Problem: "Network unreachable" eller timeout

**Möjliga orsaker:**
1. Firewall blockerar port 8883
2. Internetanslutning saknas
3. HiveMQ cluster är pausad/stoppad

**Lösning:**
```bash
# Testa nätverksanslutning
ping 7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud

# Testa port
nc -zv 7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud 8883

# Kontrollera HiveMQ Console att cluster är active
```

### Problem: "Certificate verification failed"

**Lösning:**
```bash
# Uppdatera CA certificates
sudo apt-get update
sudo apt-get install ca-certificates

# Installera certifi för Python
source genio-env/bin/activate
pip install --upgrade certifi
```

### Problem: Meddelanden skickas men tas inte emot

**Kontrollera:**
1. Topic-namn är korrekt
2. n8n är ansluten till samma broker
3. n8n subscribar på rätt topic
4. QoS-nivå är kompatibel

**Debug med HiveMQ Web Client:**
```
1. Öppna HiveMQ Console → Web Client
2. Connect med dina credentials
3. Subscribe på #  (alla topics)
4. Kör Genio AI och se meddelanden i realtid
```

## Integration med n8n

### n8n MQTT Node Configuration

```json
{
  "protocol": "mqtts",
  "host": "7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud",
  "port": 8883,
  "username": "ditt_hivemq_användarnamn",
  "password": "ditt_hivemq_lösenord",
  "clientId": "n8n-genio",
  "topic": "genio/commands"
}
```

### Exempel: n8n Workflow

**1. MQTT Trigger Node**
- Topic: `genio/commands`
- Lyssnar på röstkommandon från Genio AI

**2. Processing Nodes**
- Bearbetar kommandot
- Anropar AI/API
- Genererar svar

**3. MQTT Out Node**
- Topic: `genio/responses`
- Skickar svar tillbaka till Genio AI

## Testing Scenarios

### Test 1: Grundläggande Anslutning
```bash
python test_mqtt.py
```
Förväntat: ✅ Connection successful

### Test 2: Publish/Subscribe
```bash
# Terminal 1: Starta Genio AI
python src/main.py

# Terminal 2: Övervaka i HiveMQ Web Client
# Eller använd mosquitto_sub:
mosquitto_sub -h 7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud \
  -p 8883 -u "username" -P "password" \
  -t "genio/#" --capath /etc/ssl/certs/
```

### Test 3: End-to-End med n8n
1. Konfigurera n8n MQTT trigger för `genio/commands`
2. Konfigurera n8n MQTT output för `genio/responses`
3. Säg wake word till Genio AI
4. Ge ett kommando
5. Verifiera i n8n att meddelandet togs emot
6. n8n skickar svar
7. Genio AI talar upp svaret

## Performance Tips

### Optimal Settings

```yaml
mqtt:
  port: 8883
  use_tls: true
  # Använd QoS 1 för viktiga meddelanden
  # QoS 0 är snabbare men mindre tillförlitlig
```

### HiveMQ Cloud Limits (Free Tier)

- **Max Connections:** 100 samtidiga
- **Max Message Rate:** 100 msg/sec
- **Max Message Size:** 256 KB
- **Data Transfer:** 10 GB/månad

För produktionsmiljö, överväg betalplan om limits överskrids.

## Quick Reference Commands

```bash
# Testa MQTT-anslutning
python test_mqtt.py

# Starta Genio AI med MQTT
python src/main.py

# Övervaka MQTT med mosquitto (om installerat)
mosquitto_sub -h 7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud \
  -p 8883 -u "user" -P "pass" -t "genio/#" --capath /etc/ssl/certs/

# Publicera test-meddelande
mosquitto_pub -h 7dab69000883410aba47967fb078d6d9.s1.eu.hivemq.cloud \
  -p 8883 -u "user" -P "pass" -t "genio/test" -m "Hello from CLI" \
  --capath /etc/ssl/certs/
```

## Support

**HiveMQ Support:**
- 📖 [HiveMQ Documentation](https://docs.hivemq.com/hivemq-cloud/)
- 💬 [HiveMQ Community Forum](https://community.hivemq.com/)
- 📧 [HiveMQ Support](https://www.hivemq.com/support/)

**Genio AI:**
- 📖 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- 📖 [QUICKSTART.md](QUICKSTART.md)

---

**Genio AI** 🤖 × **HiveMQ Cloud** ☁️
