#!/bin/bash
# Genio AI - Installationsscript
# Detta script installerar Genio AI med alla beroenden i en virtuell miljö

set -e  # Avsluta vid fel

echo "🤖 Genio AI - Installation"
echo "=========================="
echo ""

# Färger för output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funktion för att skriva ut meddelanden
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Kontrollera Python-version
print_info "Kontrollerar Python-version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 är inte installerat!"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
print_success "Python $PYTHON_VERSION hittades"

# Kontrollera om vi är i rätt katalog
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt hittades inte!"
    print_info "Kör detta script från raspberry-pi-voice-agent mappen"
    exit 1
fi

# Skapa virtuell miljö
print_info "Skapar virtuell miljö..."
if [ -d "genio-env" ]; then
    print_info "Virtuell miljö finns redan, använder befintlig..."
else
    python3 -m venv genio-env
    print_success "Virtuell miljö skapad"
fi

# Aktivera virtuell miljö
print_info "Aktiverar virtuell miljö..."
source genio-env/bin/activate
print_success "Virtuell miljö aktiverad"

# Uppgradera pip
print_info "Uppgraderar pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "Pip uppgraderad"

# Installera systempaket för PyAudio
print_info "Installerar systempaket för PyAudio..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update > /dev/null 2>&1
    sudo apt-get install -y portaudio19-dev python3-pyaudio > /dev/null 2>&1
    print_success "Systempaket installerade"
else
    print_info "apt-get hittades inte, hoppar över systempaket"
fi

# Installera Python-dependencies
print_info "Installerar Python-paket från requirements.txt..."
pip install -r requirements.txt
print_success "Python-paket installerade"

# Kontrollera om Piper finns
print_info "Kontrollerar Piper TTS..."
if ! command -v piper &> /dev/null; then
    print_info "Piper TTS hittades inte, installerar..."
    
    # Avgör arkitektur
    ARCH=$(uname -m)
    if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
        PIPER_URL="https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz"
    elif [ "$ARCH" = "armv7l" ]; then
        PIPER_URL="https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_armv7l.tar.gz"
    elif [ "$ARCH" = "x86_64" ]; then
        PIPER_URL="https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz"
    else
        print_error "Okänd arkitektur: $ARCH"
        exit 1
    fi
    
    # Ladda ner och installera Piper
    wget -q $PIPER_URL -O piper.tar.gz
    tar -xzf piper.tar.gz
    sudo mv piper/piper /usr/local/bin/
    sudo chmod +x /usr/local/bin/piper
    rm -rf piper piper.tar.gz
    print_success "Piper TTS installerad"
else
    print_success "Piper TTS finns redan"
fi

# Skapa models-mapp
print_info "Skapar models-mapp..."
mkdir -p models
print_success "Models-mapp skapad"

# Ladda ner svensk röstmodell om den inte finns
if [ ! -f "models/sv_SE-nst-medium.onnx" ]; then
    print_info "Laddar ner svensk röstmodell (detta kan ta ett tag)..."
    cd models
    wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx
    wget -q https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json
    cd ..
    print_success "Svensk röstmodell nedladdad"
else
    print_success "Svensk röstmodell finns redan"
fi

# Skapa logs-mapp
print_info "Skapar logs-mapp..."
mkdir -p logs
print_success "Logs-mapp skapad"

# Skapa .env fil om den inte finns
if [ ! -f ".env" ]; then
    print_info "Skapar .env fil från .env.example..."
    cp .env.example .env
    print_success ".env fil skapad"
    print_info "⚠️  VIKTIGT: Redigera .env och lägg till din PORCUPINE_ACCESS_KEY!"
else
    print_success ".env fil finns redan"
fi

# Sammanfattning
echo ""
echo "================================"
echo -e "${GREEN}✓ Installation klar!${NC}"
echo "================================"
echo ""
echo "Nästa steg:"
echo "1. Skaffa Porcupine Access Key från https://console.picovoice.ai/"
echo "2. Redigera .env och lägg till din PORCUPINE_ACCESS_KEY"
echo "3. Redigera config/config.yaml med dina MQTT-inställningar"
echo "4. Aktivera miljön: source genio-env/bin/activate"
echo "5. Testa wake word: python test_wakeword.py"
echo "6. Testa TTS: python test_piper.py"
echo "7. Kör Genio AI: python src/main.py"
echo ""
echo "För att deaktivera virtuell miljö: deactivate"
echo ""

# Visa konfigurationstips
print_info "Viktiga konfigurationsinställningar:"
echo "  .env fil:"
echo "    - PORCUPINE_ACCESS_KEY (KRÄVS!)"
echo "    - MQTT_BROKER, MQTT_USERNAME, MQTT_PASSWORD"
echo ""
echo "  config/config.yaml:"
echo "    - MQTT broker: Uppdatera broker-adressen"
echo "    - MQTT port: 8883 (TLS/SSL)"
echo "    - Wake word: 'porcupine' (standard, gratis)"
echo ""

print_success "Genio AI är redo att användas! 🚀"
