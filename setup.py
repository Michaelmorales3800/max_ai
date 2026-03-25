"""
setup.py — MAX AI Setup Script
Run this ONCE to install all dependencies.
"""

import subprocess
import sys
import os

PACKAGES = [
    ("pyttsx3",  "Text-to-speech (voice for MAX)"),
    ("vpython",  "3D Avatar in browser"),
]

def install(package: str, description: str):
    print(f"\n📦 Installing {package} ({description})...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"   ✅ {package} installed!")
    else:
        print(f"   ⚠️  {package} failed. Error:\n{result.stderr[:300]}")

def check_ollama():
    print("\n🔍 Checking Ollama...")
    import urllib.request, urllib.error
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=3)
        print("   ✅ Ollama is running!")
    except Exception:
        print("   ⚠️  Ollama is NOT running. Start it with:")
        print("      ollama serve")
        print("      ollama pull llama3")

def main():
    print("=" * 50)
    print("  MAX AI — Setup")
    print("=" * 50)
    print(f"  Python: {sys.version}")
    print(f"  Platform: {sys.platform}")

    for pkg, desc in PACKAGES:
        install(pkg, desc)

    check_ollama()

    print("\n" + "=" * 50)
    print("  Setup complete! Run MAX with:")
    print("  python max.py")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
