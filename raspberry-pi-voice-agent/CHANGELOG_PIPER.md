# Genio AI - Uppdateringar & Piper TTS Integration

## Versionshistorik

### Version 2.0 - Genio AI Rebranding (Oktober 2025)
- 🎨 **Namnbyte:** Applikationen heter nu officiellt **Genio AI**
- 📝 Uppdaterat alla filer med nytt namn
- 🔧 Uppdaterat MQTT-topics till `genio/agent` och `genio/commands`
- 📊 Uppdaterat loggfil till `logs/genio_ai.log`
- 🔄 Bytt huvudklass från `VoiceAgent` till `GenioAI`

### Version 1.5 - Piper TTS Integration (Oktober 2025)
- 🎯 **Implementerat Piper TTS** som primär text-till-tal-motor
- ⚡ Betydligt förbättrad prestanda och ljudkvalitet
- 🔌 Offline-kapacitet - ingen internetanslutning krävs
- 🇸🇪 Stöd för högkvalitativa svenska röster

## Sammanfattning av ändringar

Genio AI-applikationen har uppdaterats för att använda **Piper TTS** som text-till-tal-motor istället för den tidigare gTTS-implementationen.

## Ändrade filer

### 1. `requirements.txt`
- **Borttaget:** `gTTS`, `playsound`
- **Tillagt:** `piper-tts`
- Piper är en lokal, offline TTS-motor som ger högre kvalitet och snabbare respons

### 2. `config/config.yaml`
- Uppdaterat TTS-konfiguration med Piper-specifika inställningar:
  ```yaml
  tts:
    engine: "piper"
    voice: "sv_SE-nst-medium"
    model_path: "models/sv_SE-nst-medium.onnx"
    config_path: "models/sv_SE-nst-medium.onnx.json"
  ```

### 3. `src/tts/tts_engine.py`
- **Fullständig omskrivning** av TTS-klassen
- Implementerat `PiperTTS` klass med följande metoder:
  - `synthesize()`: Genererar ljuddata från text
  - `speak()`: Syntetiserar och spelar upp text
  - `save_to_file()`: Sparar tal till WAV-fil
  - `set_language()`: Uppdaterar språkinställning
- Använder subprocess för att köra Piper binary
- Integrerar med sounddevice för ljuduppspelning

### 4. `src/config/settings.py`
- Lagt till dynamisk laddning av YAML-konfiguration
- Nya TTS-relaterade inställningar:
  - `TTS_MODEL_PATH`
  - `TTS_CONFIG_PATH`
  - `TTS_VOICE`
- Förbättrad MQTT-konfiguration med användarnamn/lösenord
- Lagt till loggningsinställningar från config.yaml

### 5. `src/main.py`
- Uppdaterat import för att använda `PiperTTS`
- Initialiserar TTS med korrekt modell och konfigurationssökvägar
- Skickar TTS-instans till Speaker
- Lagt till MQTT-autentisering

### 6. `README.md`
- Uppdaterat Features-sektion för att nämna Piper TTS
- Lagt till detaljerade installationsinstruktioner för:
  - Piper binary installation
  - Svenska röstmodeller nedladdning
  - Steg-för-steg setup guide

## Nya filer

### 7. `test_piper.py`
- Testskript för att verifiera Piper TTS-installation
- Testar både uppspelning och filsparning
- Hjälpsamma felmeddelanden vid problem

### 8. `PIPER_INSTALLATION.md`
- Omfattande installationsguide på svenska
- Beskriver olika svenska röstmodeller (low/medium/high)
- Prestandatips för olika Raspberry Pi-modeller
- Felsökningssektion
- Jämförelse med andra TTS-motorer

## Fördelar med Piper TTS

1. **Högkvalitativt ljud**: Neurala nätverk ger naturligt klingande tal
2. **Snabb**: Realtidssyntes även på Raspberry Pi 4/5
3. **Offline**: Fungerar helt utan internetanslutning
4. **Låg latens**: Mycket snabbare än molnbaserade lösningar som gTTS
5. **Låg CPU-användning**: Optimerad för ARM-arkitektur

## Installation

För att använda den uppdaterade applikationen, följ dessa steg:

```bash
# 1. Installera Piper binary
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
tar -xzf piper_arm64.tar.gz
sudo mv piper/piper /usr/local/bin/
sudo chmod +x /usr/local/bin/piper

# 2. Ladda ner svensk röstmodell
cd raspberry-pi-voice-agent/models
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json

# 3. Installera Python-dependencies
cd ..
pip install -r requirements.txt

# 4. Testa installationen
python test_piper.py

# 5. Kör applikationen
python src/main.py
```

## Testning

Kör testskriptet för att verifiera installationen:
```bash
python test_piper.py
```

Detta kommer att:
- Initialisera Piper TTS
- Spela upp ett testmeddelande på svenska
- Spara ljud till `test_output.wav`

## Nästa steg

1. Ladda ner önskad röstmodell (se PIPER_INSTALLATION.md)
2. Uppdatera `config/config.yaml` med korrekta sökvägar
3. Kör `test_piper.py` för att verifiera
4. Starta applikationen med `python src/main.py`

## Support

För mer information, se:
- `PIPER_INSTALLATION.md` - Detaljerad installationsguide
- `README.md` - Projektöversikt
- [Piper GitHub](https://github.com/rhasspy/piper) - Officiell dokumentation
