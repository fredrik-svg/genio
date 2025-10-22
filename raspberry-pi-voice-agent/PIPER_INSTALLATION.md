# Piper TTS Installation Guide för Raspberry Pi

## Översikt
Denna guide hjälper dig att installera och konfigurera Piper TTS på din Raspberry Pi för svensk talsyntes.

## Vad är Piper?
Piper är en snabb, lokal neural text-till-tal-motor som är optimerad för att köra på enheter som Raspberry Pi. Den erbjuder:
- Högkvalitativt, naturligt ljud
- Snabb syntes (realtid på Raspberry Pi)
- Fungerar helt offline
- Stöd för många språk inklusive svenska

## Systemkrav
- Raspberry Pi 4 eller 5 (rekommenderat)
- Raspberry Pi OS (64-bit rekommenderas)
- Minst 1 GB ledigt diskutrymme
- Python 3.8 eller senare

## Installationssteg

### 1. Installera Piper Binary

```bash
# Ladda ner Piper för ARM64 (Raspberry Pi 4/5)
cd ~
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz

# Packa upp
tar -xzf piper_arm64.tar.gz

# Flytta till systemets bin-katalog
sudo mv piper/piper /usr/local/bin/
sudo chmod +x /usr/local/bin/piper

# Verifiera installationen
piper --version
```

### 2. Ladda ner Svenska Röstmodeller

Piper erbjuder flera svenska röster. Vi rekommenderar `sv_SE-nst-medium` för bästa balans mellan kvalitet och prestanda.

```bash
# Navigera till projektets models-katalog
cd raspberry-pi-voice-agent/models

# Ladda ner mediumkvalitet modell (rekommenderad)
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json
```

#### Alternativa svenska röster:

**Låg kvalitet (snabbast, mindre fil):**
```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/low/sv_SE-nst-low.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/low/sv_SE-nst-low.onnx.json
```

**Hög kvalitet (bäst ljud, långsammare):**
```bash
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/high/sv_SE-nst-high.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/high/sv_SE-nst-high.onnx.json
```

### 3. Installera Python-beroenden

```bash
cd raspberry-pi-voice-agent
pip install -r requirements.txt
```

### 4. Konfigurera applikationen

Redigera `config/config.yaml` och uppdatera TTS-inställningarna:

```yaml
tts:
  enabled: true
  engine: "piper"
  language: "sv"
  voice: "sv_SE-nst-medium"  # Ändra baserat på vald modell
  model_path: "models/sv_SE-nst-medium.onnx"
  config_path: "models/sv_SE-nst-medium.onnx.json"
```

### 5. Testa installationen

Kör testskriptet för att verifiera att allt fungerar:

```bash
python test_piper.py
```

Du bör höra en svensk röst som säger: "Hej! Detta är ett test av Piper text-till-tal-systemet."

## Testa Piper direkt från kommandoraden

```bash
# Enkel test
echo "Hej, jag heter Piper och jag talar svenska" | piper \
  --model models/sv_SE-nst-medium.onnx \
  --output_file test.wav

# Spela upp filen
aplay test.wav
```

## Prestandatips

1. **Använd rätt modell för din hårdvara:**
   - Raspberry Pi 3: Använd `low` kvalitet
   - Raspberry Pi 4: Använd `medium` kvalitet
   - Raspberry Pi 5: Använd `medium` eller `high` kvalitet

2. **Optimera för realtid:**
   - Medium-modellen ger bra balans mellan kvalitet och hastighet
   - På Raspberry Pi 5 kan du ofta använda high-quality modellen

3. **Spara CPU:**
   - Piper är mycket mer CPU-effektivt än alternativ som Festival eller eSpeak-ng med MBROLA

## Felsökning

### "Command not found: piper"
- Kontrollera att piper är i din PATH: `which piper`
- Prova att köra med full sökväg: `/usr/local/bin/piper --version`

### "Model file not found"
- Verifiera att modellfilerna finns: `ls -la models/`
- Kontrollera sökvägarna i `config/config.yaml`

### "ONNX Runtime error"
- Installera ONNX Runtime: `pip install onnxruntime`

### Dålig ljudkvalitet eller hackig uppspelning
- Prova en lägre kvalitetsmodell
- Kontrollera att din Raspberry Pi inte är överbelastad
- Justera ljudbufferstorleken i sounddevice-inställningarna

## Ytterligare resurser

- [Piper GitHub](https://github.com/rhasspy/piper)
- [Piper Voice Samples](https://rhasspy.github.io/piper-samples/)
- [Alla tillgängliga röster](https://huggingface.co/rhasspy/piper-voices)

## Jämförelse med andra TTS-motorer

| Motor | Kvalitet | Hastighet | Offline | CPU-användning |
|-------|----------|-----------|---------|----------------|
| Piper | Hög | Snabb | ✓ | Låg |
| gTTS | Medel | Långsam | ✗ | Mycket låg |
| eSpeak | Låg | Mycket snabb | ✓ | Mycket låg |
| Festival | Medel | Medel | ✓ | Medel |

Piper erbjuder bästa kombinationen av kvalitet och prestanda för lokal talsyntes på Raspberry Pi.
