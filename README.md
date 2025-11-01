# Local Voice Assistant – Offline AI Voice Commands with Local LLM

A fully local, privacy-preserving voice assistant that continuously listens for wake words, processes your voice commands using state-of-the-art speech recognition (Whisper), generates intelligent responses (Ollama-hosted LLM), and speaks replies using offline text-to-speech. No cloud required.

## Features

- **Wake Word Detection:** Fast, hands-free activation with customizable wake words (OpenWakeWord or Porcupine).
- **Speech Recognition:** High-accuracy, multilingual transcription using Whisper (all models supported).
- **Local Language Model:** Runs Llama3, Mistral, or other models with Ollama; fully offline.
- **Text-to-Speech:** Replies read aloud using pyttsx3 (cross-platform) or neural voices (Coqui/TTS).
- **Privacy:** All processing (audio, text, LLM) occurs entirely on your device.
- **Customizable:** Swap models, change wake words, tweak voices, and extend functionality (smart home, apps).
- **No Internet Needed:** Only required for downloading dependencies/models.


## System Architecture

```mermaid
graph TD;
    A[Audio Input (Microphone)] --> B[Audio Buffer (PyAudio)];
    B --> C[Wake Word Detection (OpenWakeWord)];
    C --> D[Speech Recognition (Whisper)];
    D --> E[LLM Processing (Ollama)];
    E --> F[Text-to-Speech (pyttsx3/Coqui)];
    F --> G[Audio Output (Speakers)];
```


## Installation

### Requirements

- **OS:** Linux, macOS, Windows (Python 3.9+)
- **CPU:** Intel i5/Ryzen 5+ (\>=8GB RAM; 16GB+ recommended)
- **Audio:** USB microphone \& speakers
- **GPU:** (Optional) For faster Whisper or TTS inference


### Instructions

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv ffmpeg portaudio19-dev python3-pyaudio

# Create and activate virtual environment
python3 -m venv voice_env
source voice_env/bin/activate

# Python packages
pip install openai-whisper pyttsx3 pyaudio requests numpy webrtcvad

# Advanced (optional)
pip install openwakeword TTS speech_recognition

# Install Ollama (local LLM server)
curl -fsSL https://ollama.com/install.sh | sh

# Download LLM model
ollama pull llama3.2:3b
```


## Usage

1. **Start Ollama LLM server:**

```bash
ollama serve
# (Optionally test with: ollama run llama3.2:3b)
```

2. **Run the Voice Assistant:**

```bash
python voice_assistant.py
```

3. **Speak a wake word (e.g., “Hey Assistant”, “Computer”), then your command.**
4. **Listen for the reply!**

## Python Example Snippet

```python
# Core workflow: Wake word ➔ Whisper ➔ Ollama ➔ TTS
from openwakeword.model import Model
import whisper, pyttsx3, pyaudio

# (See voice_assistant_implementation_guide.md for complete code!)
```


## Configuration

- Edit `voice_assistant.py` for:
    - Model selection (`llama3.2:3b`, `mistral:7b`, etc.)
    - Wake word customization
    - Voice settings for TTS
    - Hardware/audio settings


## Advanced

- Add smart home or local app integration with Python modules (e.g., Home Assistant API)
- Use neural TTS for lifelike voices (`pip install TTS`)
- Train custom wake words with OpenWakeWord
- Multilingual support via Whisper


## Troubleshooting

- **Audio Issues:** Check microphone permissions/`pyaudio` config.
- **LLM Errors:** Ensure Ollama is running on `localhost:11434` and correct model is downloaded.
- **Performance:** Use smaller Whisper models or enable GPU acceleration.


## Credits

- **Whisper:** OpenAI
- **Ollama:** Local LLM platform
- **pyttsx3 / Coqui-TTS:** Offline TTS engines
- **OpenWakeWord / Porcupine:** Wake word detection