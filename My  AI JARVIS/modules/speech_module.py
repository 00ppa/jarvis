"""
JARVIS Speech Module
Handles voice input (speech recognition) and output (text-to-speech)
Uses threading for smooth, non-blocking speech output.
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue
import time

# ============================================
# TEXT-TO-SPEECH CONFIGURATION (Threaded)
# ============================================

class SpeechEngine:
    """Threaded TTS engine for smooth speech output."""
    
    def __init__(self):
        self._speech_queue = queue.Queue()
        self._running = True
        self._preferred_voice_id = None
        
        # Find preferred voice
        try:
            temp_engine = pyttsx3.init()
            for voice in temp_engine.getProperty('voices'):
                if any(name in voice.name.lower() for name in ["zira", "eva", "female", "hazel"]):
                    self._preferred_voice_id = voice.id
                    break
            if not self._preferred_voice_id:
                print("⚠️ Warning: No female voice found! Using default.")
            temp_engine.stop()
            del temp_engine
        except Exception as e:
            print(f"⚠️ Voice detection error: {e}")
        
        # Start speech thread
        self._thread = threading.Thread(target=self._speech_worker, daemon=True)
        self._thread.start()
    
    def _speech_worker(self):
        """Background worker that processes speech queue."""
        while self._running:
            try:
                # Wait for text with timeout to allow checking _running
                text = self._speech_queue.get(timeout=0.5)
                if text is None:  # Shutdown signal
                    break
                
                # Create fresh engine for each speech
                engine = pyttsx3.init()
                if self._preferred_voice_id:
                    engine.setProperty('voice', self._preferred_voice_id)
                engine.setProperty("rate", 180)
                engine.setProperty("volume", 1.0)
                engine.say(text)
                engine.runAndWait()
                engine.stop()
                del engine
                
                # Small delay between speeches
                time.sleep(0.1)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"⚠️ TTS Error: {e}")
    
    def speak(self, text):
        """Add text to speech queue (non-blocking)."""
        print(f"🤖 JARVIS: {text}")
        self._speech_queue.put(text)
    
    def speak_sync(self, text):
        """Speak immediately and wait (blocking) - for startup messages."""
        print(f"🤖 JARVIS: {text}")
        try:
            engine = pyttsx3.init()
            if self._preferred_voice_id:
                engine.setProperty('voice', self._preferred_voice_id)
            engine.setProperty("rate", 180)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            del engine
        except Exception as e:
            print(f"⚠️ TTS Error: {e}")
    
    def wait_until_done(self):
        """Wait for all queued speech to complete."""
        while not self._speech_queue.empty():
            time.sleep(0.1)
    
    def shutdown(self):
        """Stop the speech engine."""
        self._running = False
        self._speech_queue.put(None)  # Signal to stop


# Global speech engine instance
_speech_engine = None

def _get_engine():
    """Get or create the speech engine."""
    global _speech_engine
    if _speech_engine is None:
        _speech_engine = SpeechEngine()
    return _speech_engine

def speak(text):
    """Convert text to speech (non-blocking, queued)."""
    _get_engine().speak(text)

def speak_sync(text):
    """Convert text to speech (blocking, immediate)."""
    _get_engine().speak_sync(text)

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
    # Wait for any ongoing speech to finish
    _get_engine().wait_until_done()
    
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
