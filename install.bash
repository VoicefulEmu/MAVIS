#!/bin/bash

# Voice Assistant Installation Script

echo "Installing Local Voice Assistant Dependencies..."

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-venv ffmpeg portaudio19-dev python3-pyaudio

# Create virtual environment
python3 -m venv voice_assistant_env
source voice_assistant_env/bin/activate

# Install Python packages
pip install --upgrade pip

# Core packages
pip install openai-whisper
pip install pyttsx3
pip install pyaudio
pip install requests
pip install numpy
pip install webrtcvad

# Advanced packages (optional)
pip install openwakeword
pip install TTS
pip install speech_recognition

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download a model
ollama pull llama3.2:3b

echo "Installation complete!"
echo "Activate the environment with: source voice_assistant_env/bin/activate"
echo "Run the assistant with: python voice_assistant.py"
