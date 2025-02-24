```markdown
🤖 IA Integraded Voice Assistant (GPT-3.5 + DeepSeek) 🎤

**Um assistente de voz inteligente que combina GPT-3.5 e DeepSeek para interações naturais!**  
Fale com sua IA usando comandos de voz e receba respostas em tempo real. Perfeito para automação doméstica, estudos ou apenas diversão! 🚀

---

## 🎥 Demonstração Rápida
- **SOON!!**
---

## ✨ Funcionalidades
- **Reconhecimento de voz** em português (pt-BR) 🎤
- **Respostas contextualizadas** usando GPT-3.5 e DeepSeek 🤖
- **Wake word personalizável** ("Book") 🔔
- **Síntese de voz** fluente com `pyttsx3` 🔊
- Suporte a **modelos locais** (DeepSeek) e **nuvem** (OpenAI) ☁️

---

## 🛠️ Pré-requisitos
- Python 3.13+
- Git e Git LFS (para baixar modelos)
- 8GB+ de VRAM (se usar DeepSeek local)
- Conta na [OpenAI](https://openai.com/) (opcional)

---

## ⚡ Instalação Passo a Passo

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/IA_integrated_VoiceChat.git
cd IA_integrated_VoiceChat
```

### 2. Configure o Ambiente Virtual
```bash
python -m venv .DeepEnv
source .DeepEnv/bin/activate  # Linux/Mac
.DeepEnv\Scripts\activate     # Windows
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Baixe o Modelo DeepSeek Local
```bash
git lfs install
git clone https://huggingface.co/deepseek-ai/deepseek-llm-7b-chat ./models/deepseek-local
```

### 5. Configure as Chaves (Opcional)
Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua-chave-openai  # Se usar GPT-3.5
```

---

## 🚀 Como Executar
```bash
python main.py --provider deepseek-local  # Usar modelo local
# ou
python main.py --provider openai         # Usar OpenAI
```

---

## 🧩 Estrutura do Projeto
```
📁 IA_integrated_VoiceChat
├── 📁 models              → Modelos de IA locais
├── 📄 main.py             → Ponto de entrada
├── 📄 voice_interface.py  → Lógica de voz
├── 📄 ai_handlers.py      → Integração com APIs
└── 📄 .env                → Chaves secretas
```

---

## ❓ FAQ
### "Como trocar a wake word?"
Edite o arquivo `voice_interface.py` e modifique a linha:
```python
if "book" in text.lower():  # Altere para sua palavra-chave
```

### "Erro ao baixar o modelo DeepSeek?"
Certifique-se de que o Git LFS está instalado:
```bash
git lfs --version
# Se faltar: sudo apt-get install git-lfs  # Linux
```

---

## 🤝 Contribua!
1. Faça um **fork** do projeto
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit suas mudanças: `git commit -m 'Adicionei algo incrível!'`
4. Push: `git push origin minha-feature`
5. Abra um **Pull Request**!

---

## 📜 Licença
-- **SOON!!**
---

Feito com ❤️ por [João Arthur Duarte(Sertoriel)] | [Meu Portfólio](https://github.com/Sertoriel)
``` 
