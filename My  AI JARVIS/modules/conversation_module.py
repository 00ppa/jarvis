"""
JARVIS Conversation Module
Handles greetings and casual conversation responses
"""

from modules.speech_module import speak

def respond_to_greetings(command):
    """
    Respond to greetings or affectionate messages.
    
    Returns:
        True if a greeting was handled, False otherwise
    """
    if "good morning" in command:
        speak("Good morning, Farhan Sir! Have a productive day ahead.")
        return True
    elif "good evening" in command:
        speak("Good evening, Farhan Sir! Hope you're doing well.")
        return True
    elif "good night" in command:
        speak("Good night, Sir. Sleep well and dream of great code!")
        return True
    elif "how are you" in command:
        speak("I'm functioning at optimal capacity, Sir! Ready to assist.")
        return True
    elif "i love you" in command:
        speak("And I am honored to serve you, Sir. Always.")
        return True
    elif "thank you" in command or "thanks" in command:
        speak("You're most welcome, Sir. It's my pleasure.")
        return True
    elif "what can you do" in command or "help" in command:
        speak("I can search the web, open applications, take notes, set reminders, and much more. Just ask, Sir!")
        return True
    
    return False
