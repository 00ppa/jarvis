from speech_module import speak

def respond_to_greetings(command):
    """Respond to greetings or affectionate messages."""
    if "good morning" in command:
        speak("Good morning, Farhan! Have a great day ahead.")
    elif "good evening" in command:
        speak("Good evening, Farhan! Hope you're doing well.")
    elif "good night" in command:
        speak("Good night, Sir. Sleep well!")
    elif "how are you" in command:
        speak("I'm always great when I'm talking to you, Sir!")
    elif "i love you" in command:
        speak("I love you too, sweety!")
