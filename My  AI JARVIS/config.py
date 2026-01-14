"""
JARVIS Configuration Module
Centralized settings, API keys, and user preferences
"""

import os
import json
from pathlib import Path

# ============================================
# PATHS
# ============================================

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VOICE_PROFILES_DIR = DATA_DIR / "voice_profiles"
FACE_PROFILES_DIR = DATA_DIR / "face_profiles"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
VOICE_PROFILES_DIR.mkdir(exist_ok=True)
FACE_PROFILES_DIR.mkdir(exist_ok=True)

# Application paths
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# ============================================
# AI PROVIDER SETTINGS
# ============================================

# Choose your AI provider: "groq" (free cloud), "ollama" (local), or "gemini"
AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")  # Default to Groq (free!)

# Groq API (FREE - get key from https://console.groq.com)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"  # Fast and powerful

# Ollama (LOCAL - install from https://ollama.com)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")  # Run: ollama pull llama3

# Gemini API (requires billing enabled)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDQ4_-3BW62VSdHJGS8TUSZ85nwpgNSp14")

# ============================================
# JARVIS SETTINGS
# ============================================

JARVIS_CONFIG = {
    # User info
    "user_name": "Farhan Sir",
    "wake_words": ["hey jarvis", "hey jarvi", "jarvis", "ok jarvis"],
    
    # Voice settings
    "speech_rate": 180,
    "speech_volume": 1.0,
    "preferred_voice": ["zira", "eva", "hazel"],  # In order of preference
    
    # Listening settings
    "listen_timeout": 5,  # Seconds to wait for speech
    "phrase_limit": 8,    # Max seconds for a phrase
    "energy_threshold": 300,  # Mic sensitivity (lower = more sensitive)
    
    # Behavior settings
    "enable_proactive": True,  # Enable proactive suggestions
    "enable_mood_detection": True,  # Detect user mood from voice
    "sass_level": 3,  # 1-5, how sarcastic JARVIS should be
    
    # Morning briefing time
    "briefing_time": "07:00",
    
    # Work mode settings
    "work_mode_apps": ["code", "notepad++", "pycharm"],
    "work_mode_sites": ["github.com", "stackoverflow.com"],
}

# ============================================
# PERSONALITY RESPONSES
# ============================================

JARVIS_PERSONALITY = {
    "greetings": [
        "Good to see you, {user}.",
        "At your service, {user}.",
        "Hello, {user}. How may I assist you today?",
        "Ready and at your command, {user}.",
    ],
    "acknowledgments": [
        "Certainly, Sir.",
        "Right away, Sir.",
        "As you wish, Sir.",
        "Consider it done, Sir.",
        "I shall attend to it immediately.",
    ],
    "errors": [
        "I apologize, Sir. I encountered an issue.",
        "Something went wrong, Sir. Let me try again.",
        "I'm afraid I couldn't complete that, Sir.",
    ],
    "sass": [
        "I could do that, but where's the fun in that, Sir?",
        "Another brilliant idea, Sir. Truly groundbreaking.",
        "Of course, Sir. What would you do without me?",
    ],
    "encouragement": [
        "You've been working hard today, Sir. Perhaps a break?",
        "Excellent progress, Sir. Keep it up!",
        "That's quite impressive, Sir.",
    ],
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def get_config_value(key, default=None):
    """Get a config value with fallback."""
    return JARVIS_CONFIG.get(key, default)

def update_config(key, value):
    """Update a config value."""
    JARVIS_CONFIG[key] = value

def load_user_preferences():
    """Load user preferences from file."""
    prefs_file = DATA_DIR / "preferences.json"
    if prefs_file.exists():
        with open(prefs_file, "r") as f:
            return json.load(f)
    return {}

def save_user_preferences(prefs):
    """Save user preferences to file."""
    prefs_file = DATA_DIR / "preferences.json"
    with open(prefs_file, "w") as f:
        json.dump(prefs, f, indent=2)
