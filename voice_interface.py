import pyttsx3
import speech_recognition as sr
import time

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_active = True
        
    def stop(self):
        self.is_active = False 

    def speak(self, text):
        """Fala o texto fornecido."""
        self.engine.say(text)
        self.engine.runAndWait()
        time.sleep(1)

    def listen(self, timeout=10):
        """Ouve o áudio e retorna o texto transcrito."""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                return self.recognizer.recognize_google(audio, language='pt-BR')
            except sr.WaitTimeoutError:
                return "timeout"
            except sr.UnknownValueError:
                return "error"
            except sr.RequestError:
                return "error"
            except Exception as e:
                print(f"Erro no reconhecimento: {e}")
                return "error"