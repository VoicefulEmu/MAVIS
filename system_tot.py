import asyncio
import logging
from dataclasses import dataclass
from typing import List, Optional, Callable

@dataclass
class VoiceAssistantConfig:
    wake_words: List[str]
    whisper_model: str = "base"
    tts_rate: int = 150
    vad_aggressiveness: int = 2
    silence_timeout: float = 2.0
    ollama_model: str = "llama3.2:3b"
    audio_sample_rate: int = 16000

class ProductionVoiceAssistant:
    def __init__(self, config: VoiceAssistantConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Initialize all components
        self._init_audio()
        self._init_speech_recognition()
        self._init_tts()
        self._init_wake_word_detection()
        self._init_llm()

        # State management
        self.is_running = False
        self.is_listening = False

    def _init_audio(self):
        """Initialize audio system"""
        self.audio = pyaudio.PyAudio()

    def _init_speech_recognition(self):
        """Initialize speech recognition"""
        self.whisper_model = whisper.load_model(self.config.whisper_model)

    def _init_tts(self):
        """Initialize text-to-speech"""
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', self.config.tts_rate)

    def _init_wake_word_detection(self):
        """Initialize wake word detection"""
        # Use OpenWakeWord or similar
        pass

    def _init_llm(self):
        """Initialize local LLM connection"""
        # Test Ollama connection
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                self.logger.info("Ollama connection successful")
            else:
                self.logger.warning("Ollama not responding")
        except:
            self.logger.error("Cannot connect to Ollama")

    async def start(self):
        """Start the voice assistant"""
        self.is_running = True
        self.logger.info("Voice assistant starting...")

        # Start background tasks
        await asyncio.gather(
            self._listen_for_wake_word(),
            self._process_commands()
        )

    async def _listen_for_wake_word(self):
        """Background task to listen for wake words"""
        while self.is_running:
            # Audio processing loop
            await asyncio.sleep(0.01)  # Small delay

    async def _process_commands(self):
        """Background task to process voice commands"""
        while self.is_running:
            # Command processing loop
            await asyncio.sleep(0.1)

    def stop(self):
        """Stop the voice assistant"""
        self.is_running = False
        self.audio.terminate()
        self.logger.info("Voice assistant stopped")

# Usage example
async def main():
    config = VoiceAssistantConfig(
        wake_words=["hey assistant", "computer"],
        whisper_model="base",
        ollama_model="llama3.2:3b"
    )

    assistant = ProductionVoiceAssistant(config)

    try:
        await assistant.start()
    except KeyboardInterrupt:
        assistant.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
