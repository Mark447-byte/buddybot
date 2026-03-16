from speech.audio_recorder import AudioRecorder
from speech.speech_to_text import SpeechToText

class VoiceInput:
    def __init__(self, recorder: AudioRecorder, stt: SpeechToText):
        self.recorder = recorder
        self.stt = stt

    def get_voice_input(self):
        audio_file = self.recorder.record_to_file()
        if audio_file:
            text = self.stt.transcribe(audio_file)
            return text
        return None
