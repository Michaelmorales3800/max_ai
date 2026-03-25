# MAX AI — Personal Assistant
> Funny. Smart. 3D avatar. Controls your computer. Powered by LLaMA 3.

---

## 📁 FILE STRUCTURE
```
max_ai/
├── max.py           ← MAIN file — run this
├── max_commands.py  ← System control (Spotify, YouTube, apps...)
├── max_memory.py    ← Conversation memory (JSON)
├── max_avatar.py    ← 3D avatar (VPython)
├── setup.py         ← Run once to install dependencies
├── requirements.txt ← pip packages
└── max_memory.json  ← Created automatically when you chat
```

---

## ✅ STEP-BY-STEP SETUP

### STEP 1 — Install Python 3.10
Download from: https://www.python.org/downloads/release/python-3100/
- During install: CHECK "Add Python to PATH"
- Verify: open PowerShell → `python --version`

---

### STEP 2 — Install Ollama
Download from: https://ollama.com/download
- Install it (Windows installer)
- Open PowerShell and run:
```powershell
ollama serve
```
Leave that window open, then open a NEW PowerShell and run:
```powershell
ollama pull llama3
```
Wait for the download (it's about 4GB). Done!

---

### STEP 3 — Open MAX folder in VS Code
- Open VS Code
- File → Open Folder → select your `max_ai/` folder
- Open the integrated terminal: Ctrl + ` (backtick)

---

### STEP 4 — Install Python packages
In the VS Code terminal (PowerShell):
```powershell
python setup.py
```
This installs:
- `pyttsx3` — free offline text-to-speech (MAX's voice)
- `vpython` — 3D avatar that opens in your browser

Or install manually:
```powershell
pip install pyttsx3 vpython
```

---

### STEP 5 — Run MAX
```powershell
python max.py
```
MAX will greet you, the 3D avatar will open in your browser, and voice output will start.

---

## 💬 HOW TO USE

### Ask anything (just type):
```
You: What's the best way to learn Python?
You: Write me a function to sort a list by second element
You: Explain async/await like I'm 5
```

### Control your computer:
```
You: open spotify
You: play lo-fi beats on spotify
You: play Python tutorial on youtube
You: google how to reverse a string in python
You: open vscode
You: open calculator
You: volume up
You: mute
```

### Single question from PowerShell (no interactive mode):
```powershell
python max.py "What is recursion?"
python max.py "Open spotify and play jazz"
```

### Meta commands:
```
voice        → toggle voice on/off
memory       → show your conversation history
clear memory → wipe all memory
help         → show all commands
quit         → exit
```

---

## 🎤 FREE TTS OPTIONS (Text-to-Speech)

MAX uses **pyttsx3** by default — it's:
- ✅ Completely FREE
- ✅ Works offline (no internet needed)
- ✅ Uses your Windows built-in voices (David, Mark, Zira)

To get better voices (optional):
1. Windows Settings → Time & Language → Speech
2. Add voices like "Microsoft David" or download new ones
3. MAX will auto-detect the best available voice

Alternative (better quality, still free):
- **Coqui TTS**: `pip install TTS` — higher quality but slower
- **Edge TTS**: `pip install edge-tts` — uses Microsoft's neural voices (needs internet)

---

## 🧊 3D AVATAR

The avatar opens automatically in your browser when you run `python max.py`.
- Cyan glowing sphere with orbiting rings
- Pulses yellow when MAX is speaking
- Orbiting satellite dot
- Built with VPython (WebGL, no extra software needed)

---

## 🧠 HOW MEMORY WORKS

Every conversation is saved to `max_memory.json`.
MAX reads recent history at startup and includes it in his context,
so he remembers:
- What you asked before
- Projects you're working on
- Your preferences and style

The memory file grows over time. To reset: type `clear memory`.

---

## ⚙️ CUSTOMIZE MAX

Open `max.py` and edit the `MAX_PERSONALITY` string to change his personality.

Change the model in `max.py`:
```python
MODEL = "llama3"       # Default — 8B parameters
MODEL = "llama3:70b"   # Bigger, smarter (needs more RAM)
MODEL = "mistral"      # Alternative, fast
MODEL = "codellama"    # Best for coding questions
```

---

## ❗ TROUBLESHOOTING

| Problem | Fix |
|---|---|
| `ollama: command not found` | Install Ollama from ollama.com |
| `Connection refused (Ollama)` | Run `ollama serve` in a separate terminal |
| `model not found` | Run `ollama pull llama3` |
| No voice | Run `pip install pyttsx3` |
| No avatar | Run `pip install vpython` |
| Slow responses | Switch to `MODEL = "mistral"` (faster) |

---

## 🚀 QUICK START (copy-paste)

```powershell
# 1. Install packages
pip install pyttsx3 vpython

# 2. Make sure Ollama is running (in a separate terminal):
ollama serve

# 3. Pull the model (first time only):
ollama pull llama3

# 4. Run MAX:
python max.py
```

---

Built with ❤️ and Python 3.10
