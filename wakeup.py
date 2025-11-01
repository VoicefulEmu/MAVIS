import openwakeword
from openwakeword.model import Model

class AdvancedVoiceAssistant(LocalVoiceAssistant):
    def __init__(self, wake_words=["hey_jarvis", "alexa"]):
        super().__init__()

        # Initialize OpenWakeWord
        self.oww_model = Model(
            wakeword_models=wake_words,
            inference_framework='onnx'
        )

    def detect_wake_word(self, audio_data):
        """Advanced wake word detection with OpenWakeWord"""
        # Convert audio to the format expected by OpenWakeWord
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

        # Get predictions
        prediction = self.oww_model.predict(audio_np)

        # Check if any wake word was detected
        for wake_word, score in prediction.items():
            if score > 0.5:  # Threshold for detection
                print(f"Wake word '{wake_word}' detected with confidence {score:.2f}")
                return True

        return False
