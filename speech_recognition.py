import speech_recognition as sr
from threading import Thread, Event

class StreamingVoiceAssistant(LocalVoiceAssistant):
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_listening = None

    def setup_continuous_recognition(self):
        """Setup continuous speech recognition"""
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        # Start background listening
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, 
            self.process_background_audio,
            phrase_time_limit=5
        )

    def process_background_audio(self, recognizer, audio):
        """Process audio in background thread"""
        try:
            # Use Whisper for recognition
            text = recognizer.recognize_whisper(audio, model="base")
            print(f"Background recognition: {text}")

            # Check if this contains a wake word + command
            if any(wake_word in text.lower() for wake_word in ["hey assistant", "computer", "jarvis"]):
                # Extract command after wake word
                command = self.extract_command(text)
                if command:
                    response = self.query_llm(command)
                    self.speak(response)

        except sr.UnknownValueError:
            pass  # No speech detected
        except sr.RequestError as e:
            print(f"Recognition error: {e}")

    def extract_command(self, full_text):
        """Extract command portion after wake word"""
        wake_words = ["hey assistant", "computer", "jarvis"]
        text_lower = full_text.lower()

        for wake_word in wake_words:
            if wake_word in text_lower:
                # Find command after wake word
                start_idx = text_lower.find(wake_word) + len(wake_word)
                command = full_text[start_idx:].strip()
                return command

        return None
