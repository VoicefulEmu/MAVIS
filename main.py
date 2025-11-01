import threading
import queue
import time
import numpy as np
import whisper
import pyttsx3
import pyaudio
import webrtcvad
from collections import deque
import requests
import json

class LocalVoiceAssistant:
    def __init__(self):
        # Initialize components
        self.wake_word_active = False
        self.recording = False

        # Audio configuration
        self.RATE = 16000
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1

        # Initialize audio
        self.audio = pyaudio.PyAudio()

        # Initialize speech recognition
        self.whisper_model = whisper.load_model("base")

        # Initialize TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)

        # Initialize VAD for wake word detection
        self.vad = webrtcvad.Vad(2)  # Aggressiveness level 0-3

        # Audio buffer for wake word detection
        self.audio_buffer = deque(maxlen=30)  # 30 frames ~ 2 seconds

        # Queues for inter-thread communication
        self.audio_queue = queue.Queue()
        self.response_queue = queue.Queue()

    def start_microphone_stream(self):
        """Start continuous microphone monitoring"""
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        print("Listening for wake word...")

        while True:
            # Read audio data
            audio_data = stream.read(self.CHUNK)

            # Add to buffer
            self.audio_buffer.append(audio_data)

            # Check for wake word (simplified - use actual wake word detection)
            if self.detect_wake_word(audio_data):
                print("Wake word detected! Listening for command...")
                self.record_command()

    def detect_wake_word(self, audio_data):
        """Simple VAD-based wake word detection"""
        # Convert to numpy array
        audio_np = np.frombuffer(audio_data, dtype=np.int16)

        # Check if speech is present
        is_speech = self.vad.is_speech(audio_data, self.RATE)

        # In a real implementation, you would use a proper wake word model
        # For now, any speech activity triggers wake word
        return is_speech

    def record_command(self):
        """Record user command after wake word"""
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        frames = []
        silent_chunks = 0
        recording = True

        while recording:
            data = stream.read(self.CHUNK)
            frames.append(data)

            # Check for silence to stop recording
            is_speech = self.vad.is_speech(data, self.RATE)
            if not is_speech:
                silent_chunks += 1
                if silent_chunks > 30:  # ~2 seconds of silence
                    recording = False
            else:
                silent_chunks = 0

        stream.stop_stream()
        stream.close()

        # Process recorded audio
        audio_data = b''.join(frames)
        self.process_speech(audio_data)

    def process_speech(self, audio_data):
        """Process recorded speech with Whisper"""
        # Save audio to temporary file
        import tempfile
        import wave

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            wf = wave.open(tmp_file.name, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(audio_data)
            wf.close()

            # Transcribe with Whisper
            result = self.whisper_model.transcribe(tmp_file.name)
            text = result["text"].strip()

            print(f"User said: {text}")

            # Process with LLM
            response = self.query_llm(text)

            # Speak response
            self.speak(response)

    def query_llm(self, text):
        """Query local Ollama LLM"""
        try:
            url = "http://localhost:11434/api/generate"
            data = {
                "model": "llama3.2:3b",
                "prompt": f"You are a helpful voice assistant. User said: '{text}'. Respond conversationally and concisely.",
                "stream": False
            }

            response = requests.post(url, json=data)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return "Sorry, I'm having trouble processing that request."

        except Exception as e:
            print(f"LLM Error: {e}")
            return "Sorry, I'm having trouble with my language model right now."

    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def run(self):
        """Start the voice assistant"""
        try:
            self.start_microphone_stream()
        except KeyboardInterrupt:
            print("\nShutting down voice assistant...")
            self.audio.terminate()

# Usage
if __name__ == "__main__":
    assistant = LocalVoiceAssistant()
    assistant.run()
