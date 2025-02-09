from speech_module import listen, speak
from browser_module import open_website, search_google, open_incognito
from system_module import open_application, close_tab, shutdown_jarvis
from conversation_module import respond_to_greetings
from auto_typing import auto_type, google_search, open_chatgpt_and_type, open_incognito_and_type, whatsapp_type_message

def execute_command(command):
    """Check and execute the given command."""
    if not command:
        return

    # Greetings and Conversation
    if respond_to_greetings(command):
        return

    # System Commands
    if "open notepad" in command:
        open_application("Notepad", ["notepad.exe"])
    elif "open calculator" in command:
        open_application("Calculator", ["calc.exe"])
    elif "close tab" in command:
        close_tab()
    elif "jarvis shutdown" in command or "stop jarvis" in command:
        shutdown_jarvis()

    # Web Commands
    elif "search" in command:
        search_query = command.replace("search", "").strip()
        if search_query:
            search_google(search_query)
        else:
            speak("What should I search for, Farhan Sir?")
    elif "open youtube" in command:
        open_website("YouTube", "https://www.youtube.com")
    elif "open instagram" in command:
        open_website("Instagram", "https://www.instagram.com")
    elif "open facebook" in command:
        open_website("Facebook", "https://www.facebook.com")
    elif "open chatgpt" in command:
        open_website("ChatGPT", "https://chat.openai.com")
    elif "open incognito mode" in command:
        open_incognito()
    elif "open incognito mode and type" in command:
        query = command.replace("open incognito mode and type", "").strip()
        open_incognito(query)

    # Auto Typing Commands
    elif 'search' in command:
        query = command.replace('search', '').strip()
        google_search(query)
    elif 'type' in command:
        text = command.replace('type', '').strip()
        auto_type(text)
    elif 'open chatgpt and type' in command:
        message = command.replace('open chatgpt and type', '').strip()
        open_chatgpt_and_type(message)
    elif 'open incognito mode and type' in command:
        query = command.replace('open incognito mode and type', '').strip()
        open_incognito_and_type(query)
    elif 'send whatsapp message' in command:
        message = command.replace('send whatsapp message', '').strip()
        whatsapp_type_message(message)

    # Fallback
    else:
        speak("Sorry, I didn't understand that, Farhan Sir.")

def main():
    """Main function to handle Jarvis' workflow."""
    speak("Hello Farhan Sir, I'm ready to assist you!")

    # Wake word only once
    speak("Say 'Hey Jarvis' to activate me.")
    while True:
        wake_word = listen()
        if wake_word and ("hey jarvis" in wake_word or "hey jarvi" in wake_word):
            speak("Yes, Sir. I'm listening.")
            break  # Exit the loop after recognizing the wake word

    # Continuous command listening without wake word
    while True:
        command = listen()
        execute_command(command)

if __name__ == "__main__":
    main()

