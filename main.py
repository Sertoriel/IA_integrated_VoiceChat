from deepseek_local import DeepSeekLocal
from voice_interface import VoiceEngine
from interface import VoiceAssistantGUI
import tkinter as tk

def start_voice_assistant(ai, voice):
    while True:
        print("Diga 'Book' para começar...")
        voice.speak("Diga Book para começar")

        # Aguarda a palavra-chave "Book"
        while True:
            text = voice.listen()
            if text and "book" in text.lower():
                break

        print("Como posso ajudar?")
        voice.speak("Como posso ajudar?")

        # Captura a pergunta do usuário
        question = voice.listen()
        if question == "timeout":
            print("Tempo limite esgotado.")
            continue
        elif question == "error":
            print("Erro no reconhecimento de voz.")
            continue

        print(f"Você: {question}")
        response = ai.generate_response(question)
        print(f"Assistente: {response}")
        voice.speak(response)

def main():
    print("Iniciando VoiceGPT com DeepSeek Local...")
    ai = DeepSeekLocal()
    voice = VoiceEngine()
    start_voice_assistant(ai, voice)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = VoiceAssistantGUI(root)
        app.set_ai(DeepSeekLocal())  # Passa a instância do AI para a GUI
        root.mainloop()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")