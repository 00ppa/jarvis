"""
JARVIS System Module
Handles system applications and OS-level controls
"""

import subprocess
import os
import pyautogui
from modules.speech_module import speak

def open_application(app_name, command):
    """Open an application by command."""
    speak(f"Opening {app_name}, Sir.")
    try:
        subprocess.Popen(command)
    except FileNotFoundError:
        speak(f"Sorry Sir, I couldn't find {app_name}.")
    except Exception as e:
        speak(f"Error opening {app_name}: {str(e)}")

def close_tab():
    """Close the current browser/application tab."""
    speak("Closing the tab, Sir.")
    pyautogui.hotkey("ctrl", "w")

def close_window():
    """Close the current window."""
    speak("Closing the window, Sir.")
    pyautogui.hotkey("alt", "F4")

def minimize_window():
    """Minimize the current window."""
    speak("Minimizing, Sir.")
    pyautogui.hotkey("win", "down")

def maximize_window():
    """Maximize the current window."""
    speak("Maximizing, Sir.")
    pyautogui.hotkey("win", "up")

def take_screenshot():
    """Take a screenshot and save it."""
    speak("Taking a screenshot, Sir.")
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot = pyautogui.screenshot()
    filepath = f"screenshot_{timestamp}.png"
    screenshot.save(filepath)
    speak(f"Screenshot saved as {filepath}")
    return filepath

def lock_screen():
    """Lock the computer screen."""
    speak("Locking the screen, Sir.")
    os.system("rundll32.exe user32.dll,LockWorkStation")

def shutdown_computer():
    """Shutdown the computer."""
    speak("Shutting down the computer, Sir. Save your work!")
    os.system("shutdown /s /t 30")

def restart_computer():
    """Restart the computer."""
    speak("Restarting the computer, Sir. Save your work!")
    os.system("shutdown /r /t 30")

def cancel_shutdown():
    """Cancel a scheduled shutdown."""
    speak("Cancelling the shutdown, Sir.")
    os.system("shutdown /a")

def shutdown_jarvis():
    """Shutdown the AI assistant."""
    speak("Shutting down, Sir. It was my pleasure serving you. Have a great day!")
    exit()
