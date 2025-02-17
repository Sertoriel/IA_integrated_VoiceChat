import os
import time
import openai
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

# Configurações iniciais
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Velocidade de fala
recognizer = sr.Recognizer()
microphone = sr.Microphone()

def transcribe_audio(filename):
    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio, language='pt-BR')
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
    except sr.RequestError:
        print("Erro no serviço de reconhecimento")
    return None

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Erro na geração de resposta: {str(e)}"

def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(1)  # Pausa após falar

def listen_for_wake_word():
    with microphone as source:
        print("Aguardando palavra-chave 'Book'...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            audio = recognizer.listen(source, phrase_time_limit=3)
            try:
                text = recognizer.recognize_google(audio, language='pt-BR')
                if "book" in text.lower():
                    return True
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("Problema no serviço de voz")
                return False

def main():
    while True:
        if listen_for_wake_word():
            print("Como posso ajudar?")
            speak_text("Como posso ajudar?")
            
            # Gravação da pergunta
            try:
                with microphone as source:
                    audio = recognizer.listen(source, timeout=10)
                    with open("input.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                
                if text := transcribe_audio("input.wav"):
                    print(f"Você: {text}")
                    response = generate_response(text)
                    print(f"Assistente: {response}")
                    speak_text(response)
                    
            except sr.WaitTimeoutError:
                print("Tempo limite esgotado")
            except Exception as e:
                print(f"Erro: {str(e)}")

if __name__ == "__main__":
    main()