"""
JARVIS Speech Module
Handles voice input (speech recognition) and output (text-to-speech)
"""

import speech_recognition as sr
import pyttsx3

# ============================================
# TEXT-TO-SPEECH CONFIGURATION
# ============================================

engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Select a female voice for JARVIS (like FRIDAY)
selected_voice = None
for voice in voices:
    if any(name in voice.name.lower() for name in ["zira", "eva", "female", "hazel"]):
        selected_voice = voice.id
        break

if selected_voice:
    engine.setProperty('voice', selected_voice)
else:
    print("⚠️ Warning: No female voice found! Using default.")

engine.setProperty("rate", 180)  # Speech rate (words per minute)
engine.setProperty("volume", 1.0)  # Max volume

def speak(text):
    """Convert text to speech with console output."""
    print(f"🤖 JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

# ============================================
# SPEECH RECOGNITION CONFIGURATION
# ============================================

recognizer = sr.Recognizer()
mic = sr.Microphone()

# Boost microphone sensitivity for better detection
with mic as source:
    recognizer.energy_threshold = 300  # Lower = more sensitive
    recognizer.dynamic_energy_threshold = True

def listen(timeout=5, phrase_limit=8):
    """
    Listen to user input and return transcribed text.
    
    Args:
        timeout: Max seconds to wait for speech to start
        phrase_limit: Max seconds for a single phrase
    
    Returns:
        Lowercase transcribed text, or empty string on failure
    """
    with mic as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            text = recognizer.recognize_google(audio).lower()
            print(f"👤 You said: {text}")
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("🚨 Speech recognition service unavailable.")
            return ""
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return ""
