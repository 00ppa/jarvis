import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
from datetime import datetime
import os
import pyautogui
import sys

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set the voice to female
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Typically, voices[1] is female


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
        except sr.RequestError:
            speak("Sorry, there was a problem with the speech recognition service.")
            return None


def execute_command(command):
    # Check the time of day for greeting
    now = datetime.now()
    hour = now.hour

    if 'good morning' in command:
        if hour < 12:
            speak("Good morning, Farhan!")
        else:
            speak("It's not morning anymore, but good day, Farhan!")
    elif 'good afternoon' in command or 'good noon' in command:
        if 12 <= hour < 18:
            speak("Good afternoon, Farhan!")
        else:
            speak("It's not afternoon anymore, but good day, Farhan!")
    elif 'good evening' in command:
        if 18 <= hour < 22:
            speak("Good evening, Farhan!")
        else:
            speak("It's not evening anymore, but good day, Farhan!")
    elif 'how are you' in command:
        speak("I'm just a program, but I'm here to help you, Farhan. How can I assist you today?")
    elif 'i love you' in command:
        speak("I love you too, sweetie!")
    elif 'hello' in command or 'hi' in command:
        speak("Hello Farhan, how can I assist you today?")
    elif 'open notepad' in command:
        subprocess.Popen(['notepad.exe'])
        speak("Opening Notepad, Sir.")
    elif 'open calculator' in command:
        subprocess.Popen(['calc.exe'])
        speak("Opening Calculator, Sir.")
    elif 'what time is it' in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}, Sir.")
    elif 'search for' in command:
        search_query = command.replace('search for', '').replace('incognito mode', '').strip()
        if search_query:
            if 'incognito mode' in command:
                speak(f"Searching for {search_query} in incognito mode, Sir.")
                subprocess.Popen([chrome_path, '--incognito', f"https://www.google.com/search?q={search_query}"])
            else:
                speak(f"Searching for {search_query}, Sir.")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
        else:
            speak("What would you like to search for, Sir?")
    elif 'open' in command:
        if 'incognito mode' in command:
            website = command.replace('open', '').replace('incognito mode', '').strip()
            if website:
                speak(f"Opening {website} in incognito mode, Sir.")
                subprocess.Popen([chrome_path, '--incognito', website])
        else:
            website = command.replace('open', '').strip()
            if website:
                speak(f"Opening {website}, Sir.")
                webbrowser.open(website)
    elif 'close tab' in command or 'close browser' in command:
        speak("Closing the current tab, Sir.")
        pyautogui.hotkey('ctrl', 'w')
    elif 'shutdown jarvis' in command or 'stop jarvis' in command:
        speak("Shutting down Jarvis now, Sir.")
        sys.exit()  # Exit the script
    elif 'open chatgpt' in command:
        webbrowser.open('https://chat.openai.com')
        speak("Opening ChatGPT, Sir.")
    elif 'type' in command:
        text_to_type = command.replace('type', '').strip()
        if text_to_type:
            speak(f"Typing {text_to_type}, Sir.")
            pyautogui.typewrite(text_to_type)
        else:
            speak("What should I type for you, Sir?")
    else:
        speak("Sorry, I cannot perform that command, Sir.")


def main():
    # Register the path to Chrome
    global chrome_path
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # Register Chrome browser
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

    while True:
        # Listen for the wake word "Hey Jarvis"
        command = listen()
        if command and ('hey jarvis' in command or 'hey jarvi' in command):
            speak("Yes, Farhan? I'm here to assist you.")
            break

    # Continuously listen for commands without needing to say "Hey Jarvis" again
    while True:
        command = listen()
        if command:
            execute_command(command)


if __name__ == "__main__":
    main()
