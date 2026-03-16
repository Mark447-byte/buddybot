import speech_recognition as sr

class SpeechToText:
    def __init__(self, mode="online", language="en-US"):
        self.mode = mode
        self.language = language
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_file):
        if not audio_file:
            return None

        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            if self.mode == "online":
                return self.recognizer.recognize_google(audio, language=self.language)
            else:
                # Placeholder for offline (e.g. Whisper)
                return "Offline transcription not implemented yet."
        except sr.UnknownValueError:
            return "BuddyBot: I could not understand the audio."
        except sr.RequestError as e:
            return f"BuddyBot Error: STT service error; {e}"
        except Exception as e:
            return f"BuddyBot Error: {str(e)}"
