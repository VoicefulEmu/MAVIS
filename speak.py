from TTS.api import TTS

class AdvancedTTS:
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
        self.tts = TTS(model_name=model_name, progress_bar=False)

    def speak_advanced(self, text, speaker_voice="female"):
        """Advanced TTS with voice selection"""
        # Generate audio
        audio_path = f"temp_audio_{int(time.time())}.wav"
        self.tts.tts_to_file(
            text=text,
            file_path=audio_path
        )

        # Play audio (you could use pygame, playsound, or system command)
        import subprocess
        subprocess.run(["aplay", audio_path])  # Linux
        # subprocess.run(["afplay", audio_path])  # macOS
        # subprocess.run(["start", audio_path], shell=True)  # Windows

        # Clean up
        import os
        os.remove(audio_path)
