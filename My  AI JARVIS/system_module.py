import subprocess
import os
import pyautogui
from speech_module import speak

def open_application(app_name, command):
    """Open an application."""
    speak(f"Opening {app_name}, Sir.")
    subprocess.Popen(command)

def close_tab():
    """Close the current browser tab."""
    speak("Closing the tab, Sir.")
    pyautogui.hotkey("ctrl", "w")

def shutdown_jarvis():
    """Shutdown the AI assistant."""
    speak("Shutting down, Sir. Have a great day!")
    exit()
