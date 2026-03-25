"""
max_commands.py — MAX's Command Manager
Handles system control: open apps, websites, Spotify, YouTube, files, etc.
"""

import subprocess
import sys
import os
import webbrowser
import re


class CommandManager:
    """Detects and executes system commands from natural language."""

    # ── Command patterns ───────────────────────────────────────────────────────
    # Each entry: (regex_pattern, handler_method_name)
    PATTERNS: list[tuple[str, str]] = [
        # Music / Spotify
        (r"\b(open|launch|start)\s+spotify\b",             "open_spotify"),
        (r"\bplay\s+(.+?)\s+on\s+spotify\b",               "spotify_search"),
        (r"\bspotify\s+(.+)\b",                            "spotify_search"),

        # YouTube
        (r"\b(open|launch|start)\s+youtube\b",             "open_youtube"),
        (r"\bplay\s+(.+?)\s+on\s+youtube\b",               "youtube_search"),
        (r"\bsearch\s+youtube\s+for\s+(.+)",               "youtube_search"),
        (r"\byoutube\s+(.+)\b",                            "youtube_search"),

        # Browser / websites
        (r"\b(open|go to|visit)\s+(https?://\S+)",         "open_url"),
        (r"\b(open|go to|visit)\s+(\w+\.\w+\S*)",         "open_url"),
        (r"\b(google|search)\s+(?:for\s+)?(.+)",           "google_search"),

        # Apps
        (r"\b(open|launch|start)\s+(notepad|notepad\+\+)", "open_notepad"),
        (r"\b(open|launch|start)\s+(calculator|calc)\b",  "open_calculator"),
        (r"\b(open|launch|start)\s+explorer\b",            "open_explorer"),
        (r"\b(open|launch|start)\s+task\s*manager\b",      "open_task_manager"),
        (r"\b(open|launch|start)\s+(vscode|vs code|code)\b","open_vscode"),
        (r"\b(open|launch|start)\s+discord\b",             "open_discord"),
        (r"\b(open|launch|start)\s+chrome\b",              "open_chrome"),
        (r"\b(open|launch|start)\s+(.+)\b",                "open_generic_app"),

        # System
        (r"\bshutdown\b",                                  "shutdown"),
        (r"\brestart\b",                                   "restart"),
        (r"\bvolume\s+up\b",                               "volume_up"),
        (r"\bvolume\s+down\b",                             "volume_down"),
        (r"\bmute\b",                                      "mute"),

        # Files
        (r"\bopen\s+file\s+(.+)",                          "open_file"),
        (r"\bcreate\s+file\s+(.+)",                        "create_file"),
    ]

    def __init__(self):
        self.is_windows = sys.platform == "win32"
        self.is_mac     = sys.platform == "darwin"
        self.is_linux   = sys.platform.startswith("linux")

    def try_execute(self, text: str) -> str | None:
        """Try to match a command. Returns response string or None if no match."""
        lower = text.lower().strip()
        for pattern, method in self.PATTERNS:
            m = re.search(pattern, lower)
            if m:
                handler = getattr(self, method, None)
                if handler:
                    try:
                        groups = m.groups()
                        return handler(*groups) if groups else handler()
                    except Exception as e:
                        return f"⚠️ Command failed: {e}"
        return None  # No command matched → goes to AI chat

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _run(self, *args) -> bool:
        try:
            subprocess.Popen(args, shell=False)
            return True
        except FileNotFoundError:
            return False

    def _run_shell(self, cmd: str) -> bool:
        try:
            subprocess.Popen(cmd, shell=True)
            return True
        except Exception:
            return False

    # ── Spotify ────────────────────────────────────────────────────────────────
    def open_spotify(self) -> str:
        if self.is_windows:
            paths = [
                os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
                r"C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_*\Spotify.exe",
            ]
            for p in paths:
                if os.path.exists(p):
                    self._run(p)
                    return "Opening Spotify! 🎵 Time to vibe."
            # Fallback: open via URI
            self._run_shell("start spotify:")
            return "Launched Spotify via URI. Let it rip! 🎶"
        elif self.is_mac:
            self._run("open", "-a", "Spotify")
            return "Opening Spotify on Mac! 🎵"
        else:
            self._run("spotify")
            return "Opening Spotify! 🎵"

    def spotify_search(self, *args) -> str:
        query = " ".join(a for a in args if a)
        url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
        webbrowser.open(url)
        return f"Searching Spotify for '{query}' 🎵 Enjoy the tunes!"

    # ── YouTube ────────────────────────────────────────────────────────────────
    def open_youtube(self) -> str:
        webbrowser.open("https://www.youtube.com")
        return "YouTube is open. Don't fall into the shorts rabbit hole, Boss. 📺"

    def youtube_search(self, *args) -> str:
        query = " ".join(a for a in args if a)
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Searching YouTube for '{query}' 🎬"

    # ── Browser / URLs ─────────────────────────────────────────────────────────
    def open_url(self, *args) -> str:
        url = next((a for a in args if a and ("." in a or "http" in a)), None)
        if not url:
            return "Couldn't figure out the URL. Try again?"
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Opening {url} 🌐"

    def google_search(self, *args) -> str:
        query = " ".join(a for a in args if a)
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Googling '{query}' for you 🔍"

    # ── Apps (Windows) ─────────────────────────────────────────────────────────
    def open_notepad(self, *args) -> str:
        if self.is_windows:
            self._run("notepad.exe")
        elif self.is_mac:
            self._run("open", "-a", "TextEdit")
        else:
            self._run("gedit") or self._run("nano")
        return "Notepad opened. Time to write stuff! ✍️"

    def open_calculator(self, *args) -> str:
        if self.is_windows:
            self._run("calc.exe")
        elif self.is_mac:
            self._run("open", "-a", "Calculator")
        else:
            self._run("gnome-calculator")
        return "Calculator up! Let's crunch some numbers 🔢"

    def open_explorer(self) -> str:
        if self.is_windows:
            self._run("explorer.exe")
        elif self.is_mac:
            self._run("open", os.path.expanduser("~"))
        else:
            self._run("nautilus")
        return "File Explorer opened 📁"

    def open_task_manager(self) -> str:
        if self.is_windows:
            self._run("taskmgr.exe")
        elif self.is_mac:
            self._run("open", "-a", "Activity Monitor")
        else:
            self._run("gnome-system-monitor")
        return "Task Manager opened. Found the RAM hog? 🐷"

    def open_vscode(self, *args) -> str:
        self._run("code") or self._run_shell("code .")
        return "VS Code launched! Time to ship some code 💻"

    def open_discord(self) -> str:
        if self.is_windows:
            path = os.path.expandvars(r"%LOCALAPPDATA%\Discord\Update.exe")
            self._run_shell(f'start discord:')
        elif self.is_mac:
            self._run("open", "-a", "Discord")
        else:
            self._run("discord")
        return "Discord opened. Try not to get too distracted 💬"

    def open_chrome(self) -> str:
        if self.is_windows:
            self._run_shell("start chrome")
        elif self.is_mac:
            self._run("open", "-a", "Google Chrome")
        else:
            self._run("google-chrome") or self._run("chromium-browser")
        return "Chrome launched! 🌐"

    def open_generic_app(self, *args) -> str:
        app = " ".join(a for a in args if a)
        if self.is_windows:
            self._run_shell(f"start {app}")
        elif self.is_mac:
            self._run("open", "-a", app)
        else:
            self._run(app)
        return f"Trying to open '{app}'... fingers crossed! 🤞"

    # ── System ─────────────────────────────────────────────────────────────────
    def shutdown(self) -> str:
        confirm = input("[MAX] You sure you want to SHUT DOWN? (yes/no): ")
        if confirm.lower() == "yes":
            if self.is_windows:
                self._run_shell("shutdown /s /t 10")
            else:
                self._run_shell("sudo shutdown -h +1")
            return "Shutting down in 10 seconds. Goodbye cruel world 👋"
        return "Shutdown cancelled. Wise choice."

    def restart(self) -> str:
        confirm = input("[MAX] You sure you want to RESTART? (yes/no): ")
        if confirm.lower() == "yes":
            if self.is_windows:
                self._run_shell("shutdown /r /t 10")
            else:
                self._run_shell("sudo shutdown -r +1")
            return "Restarting in 10 seconds. BRB! 🔄"
        return "Restart cancelled."

    def volume_up(self) -> str:
        if self.is_windows:
            # Sends volume up key via nircmd (if available) or powershell
            self._run_shell("powershell -c \"(New-Object -ComObject WScript.Shell).SendKeys([char]175)\"")
        return "Volume cranked up! 🔊"

    def volume_down(self) -> str:
        if self.is_windows:
            self._run_shell("powershell -c \"(New-Object -ComObject WScript.Shell).SendKeys([char]174)\"")
        return "Volume turned down. Peace and quiet. 🔉"

    def mute(self) -> str:
        if self.is_windows:
            self._run_shell("powershell -c \"(New-Object -ComObject WScript.Shell).SendKeys([char]173)\"")
        return "Muted! 🔇 Silence is golden."

    # ── Files ──────────────────────────────────────────────────────────────────
    def open_file(self, path: str) -> str:
        path = path.strip()
        if not os.path.exists(path):
            return f"File not found: '{path}'"
        if self.is_windows:
            os.startfile(path)
        elif self.is_mac:
            self._run("open", path)
        else:
            self._run("xdg-open", path)
        return f"Opening '{path}' 📄"

    def create_file(self, filename: str) -> str:
        filename = filename.strip()
        with open(filename, "w") as f:
            f.write("")
        return f"Created file '{filename}' ✅"

    # ── Help ───────────────────────────────────────────────────────────────────
    def help_text(self) -> str:
        return """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MAX COMMANDS (just type naturally!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🎵  "open spotify"
  🎵  "play lo-fi on spotify"
  📺  "play Python tutorial on youtube"
  🌐  "open github.com"
  🔍  "google how to center a div"
  💻  "open vscode"
  📁  "open explorer"
  🔢  "open calculator"
  📝  "open notepad"
  💬  "open discord"

  ⚙️  META COMMANDS:
      voice        — toggle voice on/off
      memory       — show conversation history
      clear memory — wipe memory
      help         — this menu
      quit         — exit MAX
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Everything else → I'll answer it with AI!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
