# GitHub Copilot Instructions for Genio AI

This document provides guidelines for GitHub Copilot when contributing to the Genio AI voice assistant project.

## Project Overview

Genio AI is an intelligent voice assistant for Raspberry Pi with Swedish language support. It features:
- Wake word detection using Porcupine
- Speech-to-text using Faster Whisper
- Text-to-speech using Piper TTS
- MQTT communication for workflow integration
- Offline-capable operation

## Code Style and Standards

### Python Style
- Follow PEP 8 style guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 120 characters for code, 80 for comments
- Use meaningful variable and function names
- Use snake_case for functions and variables
- Use PascalCase for class names

### Imports
- Group imports in this order: standard library, third-party packages, local modules
- Each group should be separated by a blank line
- Use absolute imports over relative imports when possible

### Type Hints
- Add type hints to function signatures where appropriate
- Use Python 3.8+ compatible type hints

## Project Structure

```
genio/
├── raspberry-pi-voice-agent/
│   ├── src/
│   │   ├── main.py              # Entry point
│   │   ├── config/              # Configuration management
│   │   ├── audio/               # Audio input/output
│   │   ├── wakeword/            # Wake word detection
│   │   ├── stt/                 # Speech-to-text
│   │   ├── tts/                 # Text-to-speech
│   │   ├── mqtt/                # MQTT communication
│   │   └── utils/               # Utility functions
│   ├── config/
│   │   └── config.yaml          # Main configuration file
│   ├── models/                  # AI models directory
│   ├── requirements.txt         # Python dependencies
│   └── test_*.py                # Test scripts
```

## Security Guidelines

### API Keys and Secrets
- **NEVER** hardcode API keys, passwords, or sensitive credentials in source code
- Always use environment variables or configuration files (.env, config.yaml)
- Ensure `.env` files are in `.gitignore`
- Use the settings module to access configuration: `from config.settings import VARIABLE_NAME`
- Validate that required secrets (like `PORCUPINE_ACCESS_KEY`) are present before using them

### MQTT Security
- Always use TLS/SSL for MQTT connections (port 8883)
- Store MQTT credentials in config.yaml or .env files
- Validate broker addresses to prevent connections to unintended servers

### Input Validation
- Validate all external inputs (MQTT messages, audio data, configuration)
- Handle exceptions gracefully with appropriate error messages

## Testing

### Test Files
- Test scripts are located in the root of `raspberry-pi-voice-agent/`
- Naming convention: `test_<component>.py`
- Existing test scripts:
  - `test_wakeword.py` - Wake word detection
  - `test_stt.py` - Speech-to-text
  - `test_piper.py` - Text-to-speech
  - `test_mqtt.py` - MQTT connectivity

### Testing Guidelines
- Write simple, focused test scripts that can be run independently
- Include clear output messages indicating test status
- Handle missing dependencies gracefully with helpful error messages
- Test scripts should validate configuration before running

## Dependencies

### Core Dependencies
- `pvporcupine` - Wake word detection
- `pyaudio` / `sounddevice` - Audio handling
- `faster-whisper` - Speech-to-text
- `paho-mqtt` - MQTT client
- `piper-tts` - Text-to-speech
- `PyYAML` - Configuration parsing
- `python-dotenv` - Environment variable management

### Adding New Dependencies
- Add to `requirements.txt` with version pinning where appropriate
- Document the purpose in code comments
- Ensure compatibility with Python 3.8+
- Consider Raspberry Pi ARM64 architecture compatibility

## Logging

### Logger Usage
- Use the custom Logger class from `utils.logger` instead of print statements
- Import: `from utils.logger import Logger`
- Initialize: `self.logger = Logger()`
- Methods: `logger.info()`, `logger.warning()`, `logger.error()`
- Use emoji prefixes for better readability (e.g., "🤖", "⚠️", "✅", "❌")

## Configuration

### Configuration Management
- Primary configuration: `config/config.yaml`
- Environment overrides: `.env` file (optional)
- Access via: `from config.settings import VARIABLE_NAME`
- Support both Swedish and English documentation

### Configuration Files
- `config.yaml` - Main application settings (wake word, MQTT, models)
- `.env` - Sensitive credentials (not committed to git)
- `.env.example` - Template for environment variables

## Documentation

### Code Documentation
- Add docstrings to all classes and public methods
- Use clear, concise comments for complex logic
- Document function parameters and return types

### Project Documentation
- Main documentation files are in Markdown format
- Support bilingual content (Swedish and English)
- Common documentation files:
  - `README.md` - Main project overview
  - `INSTALLATION.md` - Installation guide
  - `CONFIG_GUIDE.md` - Configuration guide
  - `TROUBLESHOOTING.md` - Common issues and solutions
  - Component-specific guides (WAKEWORD_SETUP.md, etc.)

### Documentation Style
- Use clear headings and structure
- Include code examples in documentation
- Add emoji for visual clarity (📖, 🚀, 🔧, etc.)
- Provide both quick start and detailed instructions

## Error Handling

### Best Practices
- Use try-except blocks for operations that can fail
- Provide meaningful error messages with context
- Log errors with appropriate severity levels
- Include troubleshooting hints in error messages
- Gracefully handle missing configuration or dependencies

### Common Patterns
```python
if not REQUIRED_CONFIG:
    raise ValueError(
        "REQUIRED_CONFIG is required! "
        "Add it to config/config.yaml or .env file. "
        "See documentation for details."
    )
```

## Hardware Considerations

### Raspberry Pi Specifics
- Code is primarily designed for Raspberry Pi 5 (ARM64)
- Consider resource constraints (CPU, memory)
- Optimize for real-time audio processing
- Handle GPIO and hardware interfaces appropriately

### Audio Handling
- Support for both PyAudio and sounddevice
- Handle microphone and speaker initialization gracefully
- Include proper cleanup in exception handlers

## Language Support

### Swedish Language
- Primary language support is Swedish (sv_SE)
- Wake word detection: Swedish models
- Speech recognition: Swedish language models
- Text-to-speech: Swedish voice models (Piper)
- Documentation: Mix of Swedish and English

### Internationalization
- Keep language-specific resources separate from code
- Use configuration for language selection
- Document language requirements clearly

## MQTT Integration

### Communication Patterns
- Use MQTT for external workflow communication (n8n)
- Topics should be configurable
- Handle connection failures gracefully
- Support both TLS and non-TLS connections (TLS preferred)

### Best Practices
- Validate MQTT broker configuration before connecting
- Implement reconnection logic for robustness
- Use appropriate QoS levels
- Clean up connections on shutdown

## Common Pitfalls to Avoid

1. **Virtual Environment**: Always mention using virtual environments to avoid "externally-managed-environment" errors
2. **Absolute Paths**: Use absolute paths or proper path resolution for model files
3. **Audio Devices**: Handle missing or misconfigured audio devices gracefully
4. **Missing Models**: Check for model file existence before attempting to load
5. **Configuration Errors**: Validate configuration early and provide clear error messages

## Development Workflow

1. Create virtual environment: `python3 -m venv genio-env`
2. Activate environment: `source genio-env/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure application: Edit `config/config.yaml`
5. Test components individually before integration
6. Run full application: `python src/main.py`

## Contribution Guidelines

- Make minimal, focused changes
- Test changes on Raspberry Pi hardware when possible
- Update documentation for user-facing changes
- Maintain backward compatibility where possible
- Follow existing code patterns and conventions
