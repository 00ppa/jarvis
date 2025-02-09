import speech_recognition as sr
import pyttsx3  # Text-to-Speech Engine

# Initialize the TTS engine
engine = pyttsx3.init()

# Get all available voices
voices = engine.getProperty('voices')

# Try setting a high-pitched female voice
selected_voice = None
for voice in voices:
    if "zira" in voice.name.lower() or "eva" in voice.name.lower() or "female" in voice.name.lower():
        selected_voice = voice.id
        break  # Use the first detected female voice

if selected_voice:
    engine.setProperty('voice', selected_voice)
else:
    print("Warning: No female voice found! Using default.")

engine.setProperty("rate", 190)  # Slightly faster speed
engine.setProperty("volume", 1.0)  # Max volume

def speak(text):
    """Convert text to speech."""
    print(f"Jarvis: {text}")  # Print response for debugging
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()


import speech_recognition as sr

recognizer = sr.Recognizer()
mic = sr.Microphone()

# 🔹 Boost microphone sensitivity (run once before listen)
with mic as source:
    recognizer.energy_threshold = 300  # More sensitive to low voices

def listen():
    """Listen to user input and return as text."""
    with mic as source:
        print("Listening... 🎤")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Faster noise calibration
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)  # Faster response
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("🤖 Sorry, I didn't catch that!")
            return ""
        except sr.RequestError:
            print("🚨 Speech recognition service is down.")
            return ""
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return ""

