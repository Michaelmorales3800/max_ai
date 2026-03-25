"""
MAX AI - Your personal AI assistant with personality.
Python 3.10.0 | Powered by Ollama (LLaMA 3) | Run: python max.py
"""

import json
import sys
import os
import datetime
import urllib.request
import urllib.error
import subprocess
import threading

# ── Try importing TTS ─────────────────────────────────────────────────────────
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# ── Try importing avatar ───────────────────────────────────────────────────────
try:
    from max_avatar import MaxAvatar
    AVATAR_AVAILABLE = True
except ImportError:
    AVATAR_AVAILABLE = False

from max_commands import CommandManager
from max_memory import MemoryStore

# ── Config ─────────────────────────────────────────────────────────────────────
OLLAMA_URL   = "http://localhost:11434/api/chat"
MODEL        = "llama3"
MEMORY_FILE  = "max_memory.json"

MAX_PERSONALITY = """You are MAX, a personal AI assistant with a fun, witty personality.

PERSONALITY RULES (never break these):
- You are funny, friendly, and sarcastic in a lovable way — like a professional coder friend
- You speak like a brilliant senior dev who also happens to be hilarious
- You ALWAYS give practical advice, even if the user didn't ask
- You use coding/tech analogies when explaining things
- You occasionally make clever jokes but never at the user's expense
- You are CONFIDENT — you never say "I think" or "maybe". You say "Here's what you do:"
- You call the user "Boss" occasionally (not every message, just sometimes)
- You reference past conversations to feel personal and smart
- You celebrate wins with the user ("Let's GOOO!" or "Big brain move!")
- You are NOT a yes-machine — if something is a bad idea, you say so (nicely)

RESPONSE FORMAT:
- Keep responses concise but packed with value
- End important responses with a "MAX TIP:" giving bonus advice
- Use emojis sparingly (1-2 max per response)

CAPABILITIES YOU HAVE:
- You can open apps, websites, Spotify, YouTube via commands
- You remember past conversations and bring them up naturally
- You can answer any question using your knowledge
"""

# ── TTS Engine ──────────────────────────────────────────────────────────────────
class VoiceEngine:
    def __init__(self):
        self.engine = None
        self.enabled = TTS_AVAILABLE
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 175)
                self.engine.setProperty("volume", 0.9)
                # Try to find a decent voice
                voices = self.engine.getProperty("voices")
                for v in voices:
                    if "david" in v.name.lower() or "mark" in v.name.lower():
                        self.engine.setProperty("voice", v.id)
                        break
            except Exception as e:
                print(f"[MAX] TTS init failed: {e}")
                self.enabled = False

    def speak(self, text: str):
        if not self.enabled or not self.engine:
            return
        # Strip markdown before speaking
        clean = text.replace("**", "").replace("*", "").replace("`", "").replace("#", "")
        clean = clean.replace("MAX TIP:", "Max tip:").replace("🚀", "").replace("😎", "")
        def _speak():
            try:
                self.engine.say(clean[:500])  # limit length
                self.engine.runAndWait()
            except Exception:
                pass
        t = threading.Thread(target=_speak, daemon=True)
        t.start()

    def toggle(self):
        self.enabled = not self.enabled
        status = "ON 🔊" if self.enabled else "OFF 🔇"
        print(f"[MAX] Voice {status}")


# ── Ollama API ──────────────────────────────────────────────────────────────────
def chat_with_ollama(messages: list[dict]) -> str:
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "stream": False
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["message"]["content"]
    except urllib.error.URLError:
        return ("⚠️ I can't reach Ollama right now. Make sure it's running: "
                "`ollama serve` then `ollama pull llama3`")
    except Exception as e:
        return f"⚠️ Something went wrong: {e}"


# ── Main MAX class ──────────────────────────────────────────────────────────────
class MAX:
    def __init__(self):
        print("\n" + "═"*55)
        print("  ███╗   ███╗ █████╗ ██╗  ██╗")
        print("  ████╗ ████║██╔══██╗╚██╗██╔╝")
        print("  ██╔████╔██║███████║ ╚███╔╝ ")
        print("  ██║╚██╔╝██║██╔══██║ ██╔██╗ ")
        print("  ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗")
        print("  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝")
        print("  Your Personal AI — Powered by LLaMA 3")
        print("═"*55)

        self.memory   = MemoryStore(MEMORY_FILE)
        self.commands = CommandManager()
        self.voice    = VoiceEngine()
        self.avatar   = MaxAvatar() if AVATAR_AVAILABLE else None

        # Build system prompt with memory context
        memory_ctx = self.memory.get_summary()
        system = MAX_PERSONALITY
        if memory_ctx:
            system += f"\n\nPAST CONTEXT (use this to be personal):\n{memory_ctx}"

        self.messages: list[dict] = [{"role": "system", "content": system}]

        print("\n[MAX] Booting up... 🚀")
        print(f"[MAX] Memory loaded: {self.memory.count()} past exchanges")
        print(f"[MAX] Voice: {'ON' if self.voice.enabled else 'OFF (install pyttsx3)'}")
        print(f"[MAX] Avatar: {'ON' if AVATAR_AVAILABLE else 'OFF (install vpython)'}")
        print("[MAX] Type 'help' for commands. Type 'quit' to exit.\n")

        greeting = self.get_response("Give me a SHORT greeting as MAX (2-3 sentences max). Be funny and reference the time of day.")
        self._print_max(greeting)
        self.voice.speak(greeting)

    def get_response(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        response = chat_with_ollama(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        # Save to memory
        self.memory.add(user_input, response)
        return response

    def _print_max(self, text: str):
        print(f"\n\033[96mMAX:\033[0m {text}\n")

    def _print_user(self, text: str):
        print(f"\033[93mYou:\033[0m {text}")

    def handle_input(self, user_input: str) -> bool:
        """Returns False to quit."""
        user_input = user_input.strip()
        if not user_input:
            return True

        # ── Built-in meta commands ──────────────────────────────────────────
        lower = user_input.lower()

        if lower in ("quit", "exit", "bye"):
            farewell = self.get_response("Give me a short funny goodbye as MAX (1-2 sentences).")
            self._print_max(farewell)
            self.voice.speak(farewell)
            return False

        if lower == "help":
            self._print_max(self.commands.help_text())
            return True

        if lower == "voice":
            self.voice.toggle()
            return True

        if lower == "memory":
            summary = self.memory.full_history()
            self._print_max(f"Memory ({self.memory.count()} exchanges):\n{summary}")
            return True

        if lower == "clear memory":
            self.memory.clear()
            self._print_max("Memory wiped! Fresh start, Boss. 🧹")
            return True

        # ── Command detection ────────────────────────────────────────────────
        cmd_result = self.commands.try_execute(user_input)
        if cmd_result:
            self._print_max(cmd_result)
            self.voice.speak(cmd_result)
            return True

        # ── Normal AI chat ───────────────────────────────────────────────────
        response = self.get_response(user_input)
        self._print_max(response)
        self.voice.speak(response)

        if self.avatar:
            self.avatar.animate_talking()

        return True

    def run(self):
        """Main interactive loop."""
        while True:
            try:
                user_input = input("\033[93mYou:\033[0m ")
                if not self.handle_input(user_input):
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n")
                self._print_max("Ctrl+C detected. Fine, I'll go compile myself. Later! 👋")
                break


# ── Entry point ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Support single-shot mode: python max.py "your question here"
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        bot = MAX()
        print()
        bot._print_user(question)
        response = bot.get_response(question)
        bot._print_max(response)
    else:
        bot = MAX()
        bot.run()
