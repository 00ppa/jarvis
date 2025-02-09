import pyautogui
import time
import webbrowser
import subprocess

def auto_type(text):
    time.sleep(2)
    pyautogui.write(text)
    pyautogui.press("enter")

def google_search(query):
    webbrowser.open("https://www.google.com")
    time.sleep(3)
    pyautogui.write(query)
    pyautogui.press("enter")

def open_chatgpt_and_type(message):
    webbrowser.open("https://chat.openai.com")
    time.sleep(5)
    pyautogui.write(message)
    pyautogui.press("enter")

def open_incognito_and_type(query):
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    subprocess.Popen([chrome_path, "--incognito"])
    time.sleep(3)
    pyautogui.write(query)
    pyautogui.press("enter")

def whatsapp_type_message(message):
    webbrowser.open("https://web.whatsapp.com")
    time.sleep(10)
    pyautogui.write(message)
    pyautogui.press("enter")
