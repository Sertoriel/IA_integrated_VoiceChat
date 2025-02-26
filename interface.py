# interface.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from deepseek_local import DeepSeekLocal
from voice_interface import VoiceEngine

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Painel de Controle - IA Voice Assistant")
        self.root.geometry("800x600")
        
        # Inicializa componentes principais
        self.ai = DeepSeekLocal()
        self.voice = VoiceEngine()
        self.is_listening = False
        
        # Configura tema escuro
        self.root.tk_setPalette(background='#2E2E2E', foreground='white')
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        # Frame de Controle
        control_frame = ttk.LabelFrame(self.root, text=" Controle em Tempo Real ")
        control_frame.pack(pady=10, padx=10, fill="x")

        # Botões
        self.btn_listen = ttk.Button(control_frame, text="🎤 Iniciar Escuta", command=self.toggle_listening)
        self.btn_listen.pack(side="left", padx=5)

        ttk.Button(control_frame, text="⚙️ Configurações", command=self.open_settings).pack(side="right", padx=5)

        # Status do Microfone
        self.mic_status = ttk.Label(control_frame, text="Status: Inativo")
        self.mic_status.pack(side="left", padx=20)

        # Área de Logs
        log_frame = ttk.LabelFrame(self.root, text=" Histórico de Interações ")
        log_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.log_text = tk.Text(log_frame, height=10, bg='#1E1E1E', fg='white')
        self.log_text.pack(fill="both", expand=True)

        # Painel de Status
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(status_frame, text="Modelo Ativo:").pack(side="left")
        self.model_label = ttk.Label(status_frame, text="DeepSeek-7B", foreground="#00FF00")
        self.model_label.pack(side="left", padx=5)

    def toggle_listening(self):
        self.is_listening = not self.is_listening
        if self.is_listening:
            self.btn_listen.config(text="⏹ Parar Escuta")
            threading.Thread(target=self.listen_loop).start()
        else:
            self.btn_listen.config(text="🎤 Iniciar Escuta")

    def listen_loop(self):
        while self.is_listening:
            text = self.voice.listen()
            if text:
                self.log(f"Você: {text}")
                response = self.ai.generate_response(text)
                self.log(f"Assistente: {response}")
                self.voice.speak(response)

    def log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")

    def open_settings(self):
        settings_win = tk.Toplevel()
        settings_win.title("Configurações Avançadas")
        
        # Configuração do Modelo
        ttk.Label(settings_win, text="Modelo de IA:").grid(row=0, column=0, padx=5, pady=5)
        self.model_var = tk.StringVar(value="deepseek")
        ttk.Combobox(settings_win, textvariable=self.model_var, values=["deepseek", "openai"]).grid(row=0, column=1)

        # Configuração da Wake Word
        ttk.Label(settings_win, text="Palavra de Ativação:").grid(row=1, column=0)
        self.wake_var = tk.StringVar(value="book")
        ttk.Entry(settings_win, textvariable=self.wake_var).grid(row=1, column=1)

        ttk.Button(settings_win, text="Salvar", command=self.save_settings).grid(row=2, columnspan=2, pady=10)

    def save_settings(self):
        # Lógica para alterar configurações
        self.model_label.config(text="DeepSeek-7B" if self.model_var.get() == "deepseek" else "GPT-3.5")
        messagebox.showinfo("Sucesso", "Configurações atualizadas!")

    def update_status(self):
        # Atualizações dinâmicas
        self.root.after(1000, self.update_status)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()