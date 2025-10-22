# Genio AI - Rebranding Guide 🎨

## Översikt
Applikationen har officiellt döpts om från "Raspberry Pi Voice Agent" till **Genio AI**.

## Namn och Identitet

### Varför Genio?
- **Genio** kommer från latinets "genius" - intelligent ande eller beskyddare
- Kort, minnesvärt och lätt att uttala på svenska
- Professionellt och modernt namn för en AI-assistent
- Passar perfekt för en intelligent röstassistent

### Varför AI-suffix?
- Tydliggör att det är en AI-driven assistent
- Modern och tidsenlig namngivning
- Kommunicerar produktens kärnfunktion

## Genomförda Ändringar

### 📄 Uppdaterade Filer

#### 1. README.md
- Huvudrubrik ändrad till "Genio AI 🤖"
- Lagt till badges och tagline
- Uppdaterat projektstruktur
- Förtydligat användningsflöde

#### 2. src/main.py
- Klassnamn: `VoiceAgent` → `GenioAI`
- Loggmeddelande: "Connected to MQTT broker" → "Genio AI connected to MQTT broker"

#### 3. config/config.yaml
- MQTT topic: `voice/agent` → `genio/agent`
- MQTT client ID: `raspberry_pi_voice_agent` → `genio_ai`
- Loggfil: `logs/voice_agent.log` → `logs/genio_ai.log`
- MQTT commands topic: `voice/commands` → `genio/commands`

#### 4. src/config/settings.py
- Uppdaterat standardvärden för MQTT-konfiguration
- Uppdaterat standardsökväg för loggfil

#### 5. Dokumentation
- `CHANGELOG_PIPER.md` - Lagt till versionshistorik
- `PIPER_INSTALLATION.md` - Uppdaterat rubrik
- `test_piper.py` - Uppdaterat docstring

## Tekniska Detaljer

### MQTT Topics
```yaml
Tidigare:
- voice/agent
- voice/commands

Nu:
- genio/agent
- genio/commands
```

### Klassnamn
```python
Tidigare:
class VoiceAgent:
    ...

Nu:
class GenioAI:
    ...
```

### Loggfiler
```
Tidigare: logs/voice_agent.log
Nu:       logs/genio_ai.log
```

## Migration Guide

Om du har en befintlig installation, följ dessa steg:

### 1. Uppdatera Git Repository
```bash
cd raspberry-pi-voice-agent
git pull origin main
```

### 2. Uppdatera MQTT-konfiguration
Om du har konfigurerat n8n eller andra tjänster som lyssnar på MQTT-topics:
- Ändra topic från `voice/commands` till `genio/commands`
- Ändra topic från `voice/agent` till `genio/agent`

### 3. Rensa gamla loggfiler (valfritt)
```bash
# Flytta eller ta bort gamla loggar
mv logs/voice_agent.log logs/voice_agent.log.old
```

### 4. Starta om applikationen
```bash
python src/main.py
```

## Framtida Utveckling

### Planerade Funktioner för Genio AI
- 🎙️ Förbättrad röstigenkänning
- 🧠 Konversationsminne
- 🔌 Plugin-system för utökningar
- 📱 Webbgränssnitt för administration
- 🌐 Stöd för fler språk
- 🔊 Anpassningsbara röster
- 📊 Användningsstatistik och analyser

### Roadmap
- **Version 2.1:** Förbättrad felhantering och logging
- **Version 2.2:** Webbgränssnitt för konfiguration
- **Version 3.0:** Multi-språk support och konversationsminne

## Branding Guidelines

### Logotyp och Identitet
- **Primärfärg:** #4A90E2 (Blå - intelligens och teknologi)
- **Sekundärfärg:** #50E3C2 (Turkos - innovation)
- **Ikon:** 🤖 (Robot emoji som placeholder)
- **Tagline:** "An intelligent voice assistant for Raspberry Pi"

### Tonalitet
- Professionell men tillgänglig
- Tekniskt korrekt men lättförståelig
- Vänlig och hjälpsam
- Fokus på användarvänlighet

## Support och Community

### Hjälp och Frågor
- Se dokumentation i README.md
- Kontrollera CHANGELOG_PIPER.md för senaste uppdateringar
- Läs PIPER_INSTALLATION.md för installationshjälp

### Bidrag
Bidrag till Genio AI välkomnas! Följ dessa riktlinjer:
- Använd "Genio AI" i all ny dokumentation
- Uppdatera CHANGELOG när du gör ändringar
- Följ befintlig kodstil och struktur

## Slutsats

Genio AI representerar nästa steg i projektets utveckling - från en enkel röstassistent till en intelligent AI-plattform. Namnet återspeglar vårt fokus på intelligens, användarvänlighet och modern teknik.

---

**Genio AI** - Din intelligenta röstassistent för Raspberry Pi 🤖
