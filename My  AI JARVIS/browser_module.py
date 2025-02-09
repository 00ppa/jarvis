import webbrowser
import pyautogui
import time
import subprocess
from speech_module import speak

CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

def open_website(site_name, url):
    """Open a website in the default browser."""
    speak(f"Opening {site_name}, Sir.")
    webbrowser.open(url)

def search_google(query):
    """Search Google directly."""
    speak(f"Searching Google for {query}, Sir.")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def search_youtube(query):
    """Search YouTube directly."""
    speak(f"Searching YouTube for {query}, Sir.")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def search_wikipedia(query):
    """Search Wikipedia directly."""
    speak(f"Searching Wikipedia for {query}, Sir.")
    webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")

def open_chatgpt():
    """Open ChatGPT in the browser."""
    speak("Opening ChatGPT, Sir.")
    webbrowser.open("https://chat.openai.com/")

def open_incognito(query=None):
    """Open Chrome in incognito mode and optionally type a query."""
    speak("Opening Chrome in incognito mode, Sir.")
    subprocess.Popen([CHROME_PATH, "--incognito"])
    time.sleep(2)  # Wait for Chrome to open
    if query:
        pyautogui.typewrite(query)
        pyautogui.press("enter")

def auto_type(query):
    """Type a given text automatically (for search bars, chat, etc.)."""
    speak(f"Typing {query}, Sir.")
    pyautogui.typewrite(query)
    pyautogui.press("enter")

# Predefined website shortcuts
def open_youtube():
    open_website("YouTube", "https://www.youtube.com")

def open_instagram():
    open_website("Instagram", "https://www.instagram.com")

def open_facebook():
    open_website("Facebook", "https://www.facebook.com")

def open_twitter():
    open_website("Twitter", "https://twitter.com")

def open_reddit():
    open_website("Reddit", "https://www.reddit.com")
