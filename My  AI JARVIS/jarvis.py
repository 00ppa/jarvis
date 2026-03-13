"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System
====================================================
An Iron Man-inspired AI assistant with advanced capabilities

Features:
- AI-powered conversations (Gemini)
- Voice recognition and text-to-speech
- System monitoring and control
- Productivity tools (reminders, notes, timers)
- Screen awareness and analysis
- Proactive suggestions
- Emotional intelligence
- Unique personality

Author: Farhan
Version: 2.0
"""

import sys
import datetime
import time
import os
sys.path.insert(0, '.')

# Core modules
from modules.speech_module import listen, speak
from modules.browser_module import open_website, search_google, open_incognito
from modules.system_module import (
    open_application, close_tab, shutdown_jarvis,
    take_screenshot, lock_screen
)
from modules.conversation_module import respond_to_greetings
from modules.auto_typing import (
    auto_type, google_search, open_chatgpt_and_type,
    open_incognito_and_type, whatsapp_type_message
)
from modules.system_monitor import (
    system_status, cpu_status, memory_status,
    battery_status, kill_app
)
from modules.productivity_module import (
    remind_me, take_note, set_timer, add_todo,
    get_productivity
)
from modules.telegram_module import get_telegram_bridge
from modules.calendar_module import get_calendar_manager
from modules.notion_module import get_notion_manager

# Core AI
from core.ai_brain import get_brain
from core.personality import get_personality
from core.memory_module import get_memory

# Features
from features.proactive_engine import start_proactive, morning_briefing
from features.emotion_module import detect_mood, adapt_response, get_encouragement
from features.vision_module import whats_on_screen, check_errors, help_with_code

# Config
from config import JARVIS_CONFIG, PLUGIN_CONFIG

# Plugins
from core.plugin_loader import initialize_plugins, handle_plugin_command, get_plugin_loader


def execute_command(command, speak_response=True):
    """
    Process and execute user commands.
    Uses AI brain for natural language understanding.
    Returns: Response string if any.
    """
    if not command:
        return None
    
    response_text = ""
    
    # Detect user mood
    mood = detect_mood(command)
    
    # Check for easter eggs first
    personality = get_personality()
    easter_egg = personality.check_easter_egg(command)
    if easter_egg:
        if speak_response: speak(easter_egg)
        return easter_egg
    
    # Greetings and Conversation
    if respond_to_greetings(command):
        return "Hello Sir!"
    
    # =========================================
    # PLUGIN MANAGEMENT COMMANDS
    # =========================================
    
    if "list plugins" in command or "show plugins" in command:
        loader = get_plugin_loader()
        plugins = loader.get_plugin_list()
        if plugins:
            speak(f"I have {len(plugins)} plugins loaded, Sir.")
            for p in plugins:
                speak(f"{p['name']} version {p['version']}")
        else:
            speak("No plugins are currently loaded, Sir.")
        return
    
    elif "reload plugins" in command:
        loader = get_plugin_loader()
        count = loader.reload_plugins()
        speak(f"Reloaded {count} plugins, Sir.")
        return
    
    elif "disable plugin" in command:
        plugin_name = command.replace("disable plugin", "").strip()
        if plugin_name:
            loader = get_plugin_loader()
            if loader.disable_plugin(plugin_name):
                speak(f"Disabled {plugin_name} plugin, Sir.")
            else:
                speak(f"Could not find plugin {plugin_name}, Sir.")
        else:
            speak("Which plugin should I disable, Sir?")
        return
    
    elif "enable plugin" in command:
        plugin_name = command.replace("enable plugin", "").strip()
        if plugin_name:
            loader = get_plugin_loader()
            if loader.enable_plugin(plugin_name):
                speak(f"Enabled {plugin_name} plugin, Sir.")
            else:
                speak(f"Could not find plugin {plugin_name}, Sir.")
        else:
            speak("Which plugin should I enable, Sir?")
        return
    
    # =========================================
    # PLUGIN COMMANDS (check before built-ins)
    # =========================================
    
    if PLUGIN_CONFIG.get("enabled", True):
        if handle_plugin_command(command):
            return  # Plugin handled the command
    
    # =========================================
    # SYSTEM COMMANDS
    # =========================================
    
    if "open notepad" in command:
        open_application("Notepad", ["notepad.exe"])
        return "Opening Notepad for you, Sir."
    elif "open calculator" in command:
        open_application("Calculator", ["calc.exe"])
        return "Opening Calculator, Sir."
    elif any(x in command for x in ["close tab", "close this tab"]):
        close_tab()
        return "Closing the active tab, Sir."
    elif any(x in command for x in ["jarvis shutdown", "stop jarvis", "goodbye jarvis"]):
        shutdown_jarvis()
        return "Shutting down. Goodbye, Sir."
    elif "take screenshot" in command or "screenshot" in command:
        take_screenshot()
        return "Screenshot taken, Sir."
    elif "lock screen" in command or "lock computer" in command:
        lock_screen()
        return "Locking the screen, Sir."
    
    elif "run diagnostics" in command or "system check" in command:
        from diagnostics import run_diagnostics
        run_diagnostics()
        return "Diagnostic report generated, Sir. Check the console."
    
    # =========================================
    # SYSTEM MONITORING
    # =========================================
    
    elif any(x in command for x in ["system status", "how's the system", "system health"]):
        return system_status()
    elif any(x in command for x in ["cpu status", "cpu usage"]):
        return f"CPU usage is at {cpu_status()}%, Sir."
    elif any(x in command for x in ["memory status", "ram usage", "memory usage"]):
        mem = memory_status()
        return f"Memory usage is at {mem['percent']}%, Sir."
    elif any(x in command for x in ["battery status", "battery level", "battery"]):
        return str(battery_status())
    elif "kill" in command:
        # Extract app name: "kill chrome" -> "chrome"
        app_name = command.replace("kill", "").strip()
        if app_name:
            if kill_app(app_name):
                return f"Terminated {app_name}, Sir."
            return f"I couldn't find {app_name} running, Sir."
        return "What should I kill, Sir?"
    
    # =========================================
    # PRODUCTIVITY COMMANDS
    # =========================================
    
    elif "remind me" in command:
        # Parse: "remind me to call mom in 5 minutes"
        parts = command.replace("remind me to", "").replace("remind me", "").strip()
        if " in " in parts:
            message, time_str = parts.rsplit(" in ", 1)
            remind_me(message.strip(), f"in {time_str}")
        elif " at " in parts:
            message, time_str = parts.rsplit(" at ", 1)
            remind_me(message.strip(), f"at {time_str}")
        else:
            if speak_response: speak("When should I remind you, Sir?")
            return "When should I remind you, Sir?"

    elif "schedule" in command or "appointment" in command:
        # Simple extraction: "schedule meeting at 2026-03-14T14:00:00"
        # In a real scenario, we'd use more advanced LLM parsing
        calendar = get_calendar_manager()
        response = calendar.add_event(command, datetime.datetime.now().isoformat())
        if speak_response: speak(response)
        return response
    
    elif "take a note" in command or "note this" in command:
        content = command.replace("take a note", "").replace("note this", "").strip()
        if content:
            take_note(content)
            return f"Note saved: {content}"
        else:
            if speak_response: speak("What should I note, Sir?")
            return "What should I note, Sir?"
    
    elif "set timer" in command or "set a timer" in command:
        duration = command.replace("set a timer for", "").replace("set timer for", "").replace("set timer", "").strip()
        if duration:
            set_timer(duration)
            return f"Timer set for {duration}, Sir."
        else:
            if speak_response: speak("For how long, Sir?")
            return "For how long, Sir?"
    
    elif "add to do" in command or "add todo" in command or "add to my list" in command:
        task = command.replace("add to do", "").replace("add todo", "").replace("add to my list", "").strip()
        if task:
            add_todo(task)
            # Also sync to Notion
            notion = get_notion_manager()
            notion.add_task(task)
        else:
            if speak_response: speak("What task should I add, Sir?")
            return "What task should I add, Sir?"
    
    elif "read my notes" in command or "show notes" in command:
        productivity = get_productivity()
        productivity.read_last_note()
    
    elif "read my to do" in command or "what's on my list" in command or "my tasks" in command:
        productivity = get_productivity()
        productivity.read_todos()
    
    # =========================================
    # SCREEN AWARENESS COMMANDS
    # =========================================
    
    elif any(x in command for x in ["what's on screen", "what's on my screen", "describe screen"]):
        return whats_on_screen()
    
    elif any(x in command for x in ["check for errors", "any errors", "see any errors"]):
        return check_errors()
    
    elif any(x in command for x in ["help with code", "help me code", "explain this code"]):
        return help_with_code()
    
    # =========================================
    # PROACTIVE & BRIEFING COMMANDS
    # =========================================
    
    elif any(x in command for x in ["morning briefing", "daily briefing", "brief me"]):
        return morning_briefing()
    
    elif "encourage me" in command or "motivate me" in command:
        speak(get_encouragement())
    
    # =========================================
    # WEB COMMANDS (Compound first)
    # =========================================
    
    elif 'open chatgpt and type' in command:
        message = command.replace('open chatgpt and type', '').strip()
        if message:
            open_chatgpt_and_type(message)
        else:
            speak("What should I type in ChatGPT, Sir?")
    
    elif 'open incognito mode and type' in command or 'open incognito and type' in command:
        query = command.replace('open incognito mode and type', '').replace('open incognito and type', '').strip()
        if query:
            open_incognito_and_type(query)
        else:
            speak("What should I search in incognito, Sir?")
    
    elif 'send whatsapp message' in command:
        message = command.replace('send whatsapp message', '').strip()
        if message:
            whatsapp_type_message(message)
        else:
            speak("What message should I send, Sir?")
    
    # Simple web commands
    elif "open youtube" in command:
        open_website("YouTube", "https://www.youtube.com")
        return "Opening YouTube, Sir."
    elif "open instagram" in command:
        open_website("Instagram", "https://www.instagram.com")
        return "Opening Instagram, Sir."
    elif "open facebook" in command:
        open_website("Facebook", "https://www.facebook.com")
        return "Opening Facebook, Sir."
    elif "open twitter" in command or "open x" in command:
        open_website("Twitter", "https://twitter.com")
        return "Opening X, Sir."
    elif "open github" in command:
        open_website("GitHub", "https://github.com")
        return "Opening GitHub, Sir."
    elif "open linkedin" in command:
        open_website("LinkedIn", "https://www.linkedin.com")
        return "Opening LinkedIn, Sir."
    elif "open reddit" in command:
        open_website("Reddit", "https://www.reddit.com")
        return "Opening Reddit, Sir."
    elif "open chatgpt" in command:
        open_website("ChatGPT", "https://chat.openai.com")
        return "Opening ChatGPT, Sir."
    elif "open incognito" in command:
        open_incognito()
        return "Opening browser in incognito, Sir."
    
    # Search commands
    elif "search" in command:
        search_query = command.replace("search", "").replace("for", "").strip()
        if search_query:
            search_google(search_query)
        else:
            speak("What should I search for, Sir?")
    
    # Type command
    elif "type" in command:
        text = command.replace("type", "").strip()
        if text:
            auto_type(text)
        else:
            speak("What should I type, Sir?")
    
    # =========================================
    # AI CONVERSATION (Fallback to Gemini)
    # =========================================
    
        # Use the AI brain for natural conversation
        brain = get_brain()
        response = brain.think(command)
        
        # Adapt response based on mood
        adapted_response = adapt_response(response)
        if speak_response: speak(adapted_response)
        
        # Save to memory
        memory = get_memory()
        memory.save_conversation(command, adapted_response, mood=mood)
        return adapted_response


def main():
    """Main function - JARVIS entry point."""
    
    # Get personality
    personality = get_personality()
    
    # Initialize plugins
    if PLUGIN_CONFIG.get("enabled", True):
        print("🔌 Initializing plugin system...")
        initialize_plugins(PLUGIN_CONFIG.get("disabled_plugins", []))
    
    # Initial greeting
    speak(personality.get_greeting())
    speak("All systems operational. I am ready to assist.")
    
    # Start proactive monitoring
    start_proactive()
    
    # Initialize and start Telegram Bridge
    print("📱 Initializing Telegram bridge...")
    telegram = get_telegram_bridge(brain_callback=lambda cmd: execute_command(cmd, speak_response=False))
    telegram.start()
    
    # Wake word activation
    speak("Say 'Hey Jarvis' to activate me.")
    
    while True:
        wake_word = listen()
        if wake_word:
            wake_triggers = JARVIS_CONFIG.get("wake_words", ["hey jarvis"])
            if any(trigger in wake_word for trigger in wake_triggers):
                speak(personality.get_waiting_response())
                break
    
    # Main command loop
    speak("Continuous listening mode activated. I'm at your service, Sir.")
    
    while True:
        try:
            command = listen()
            if command:
                execute_command(command)
        except KeyboardInterrupt:
            speak("Shutting down. It was my pleasure serving you, Sir.")
            break
        except Exception as e:
            print(f"Error: {e}")
            speak(personality.get_error_response())


if __name__ == "__main__":
    main()
