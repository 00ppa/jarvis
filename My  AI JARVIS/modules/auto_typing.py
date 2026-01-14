"""
JARVIS Auto Typing Module
Handles automated typing for various applications
"""

import pyautogui
import time
import webbrowser
import subprocess
from config import CHROME_PATH

def auto_type(text, delay=0.05):
    """
    Type text automatically with optional delay between characters.
    
    Args:
        text: Text to type
        delay: Delay between characters in seconds
    """
    time.sleep(1)  # Brief pause before typing
    pyautogui.write(text, interval=delay)
    pyautogui.press("enter")

def google_search(query):
    """Open Google and search for a query."""
    webbrowser.open("https://www.google.com")
    time.sleep(2)
    pyautogui.write(query)
    pyautogui.press("enter")

def open_chatgpt_and_type(message):
    """Open ChatGPT and type a message."""
    webbrowser.open("https://chat.openai.com")
    time.sleep(5)  # ChatGPT takes longer to load
    pyautogui.write(message)
    pyautogui.press("enter")

def open_incognito_and_type(query):
    """Open Chrome incognito and type a query."""
    try:
        subprocess.Popen([CHROME_PATH, "--incognito"])
        time.sleep(2)
        pyautogui.write(query)
        pyautogui.press("enter")
    except FileNotFoundError:
        print("Chrome not found!")

def whatsapp_type_message(message):
    """Open WhatsApp Web and type a message."""
    webbrowser.open("https://web.whatsapp.com")
    time.sleep(10)  # WhatsApp Web takes time to load
    pyautogui.write(message)
    # Don't auto-press enter for WhatsApp - user needs to select contact first

def youtube_search(query):
    """Open YouTube and search for a query."""
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def open_email_and_compose(to="", subject="", body=""):
    """Open Gmail compose window."""
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={to}&su={subject}&body={body}"
    webbrowser.open(gmail_url)
