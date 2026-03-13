"""
JARVIS Diagnostic Interface
Comprehensive health check for all systems
"""

import os
import sys
import time
from colorama import init, Fore, Style
from dotenv import load_dotenv

# Initialize colorama for Windows terminal
init()

def print_result(name, status, message=""):
    color = Fore.GREEN if status else Fore.RED
    symbol = "✅" if status else "❌"
    print(f"{color}{symbol} {name.ljust(20)} {message}{Style.RESET_ALL}")

def run_diagnostics():
    print(f"\n{Fore.CYAN}=== JARVIS SYSTEM DIAGNOSTICS ==={Style.RESET_ALL}\n")
    load_dotenv()
    
    # 1. Environment Check
    env_exists = os.path.exists('.env')
    print_result("Environment (.env)", env_exists, "" if env_exists else "File missing! Copy from .env.example")
    
    # 2. Module Connection Checks
    print(f"\n{Fore.YELLOW}Connecting to Modules...{Style.RESET_ALL}")
    
    # Telegram
    tg_token = os.getenv("TELEGRAM_TOKEN")
    tg_chat = os.getenv("TELEGRAM_CHAT_ID")
    print_result("Telegram Bridge", bool(tg_token and tg_chat), "Token/ChatID missing" if not (tg_token and tg_chat) else "Configured")
    
    # Cloud Sync
    notion_token = os.getenv("NOTION_TOKEN")
    notion_db = os.getenv("NOTION_DATABASE_ID")
    print_result("Notion Sync", bool(notion_token and notion_db), "Token/DB ID missing" if not (notion_token and notion_db) else "Configured")
    
    gcal_creds = os.path.exists('credentials.json')
    print_result("Google Calendar", gcal_creds, "credentials.json missing" if not gcal_creds else "Ready")
    
    # 3. Automation Validation
    print(f"\n{Fore.YELLOW}Testing Automation Skills...{Style.RESET_ALL}")
    
    try:
        from modules.system_module import open_application
        print_result("Automation Engine", True, "Link established")
        
        # Test specific app opening (User request)
        print(f"   ∟ Checking Chrome path...")
        import subprocess
        chrome_found = False
        possible_chrome_paths = [
            "chrome.exe",
            os.path.join(os.environ.get("ProgramFiles", ""), "Google/Chrome/Application/chrome.exe"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Google/Chrome/Application/chrome.exe"),
            os.path.join(os.environ.get("LocalAppData", ""), "Google/Chrome/Application/chrome.exe"),
        ]
        
        for path in possible_chrome_paths:
            if os.path.exists(path):
                print_result("  Chrome Detect", True, f"Found at: {path}")
                chrome_found = True
                break
            else:
                try:
                    subprocess.run(["where", path], capture_output=True, check=True)
                    print_result("  Chrome Detect", True, "Found in PATH")
                    chrome_found = True
                    break
                except:
                    continue
        
        if not chrome_found:
            print_result("  Chrome Detect", False, "Not found. Please install Chrome or add to PATH.")
            
    except Exception as e:
        print_result("Automation Engine", False, str(e))
    
    # 4. AI Brain Check
    print(f"\n{Fore.YELLOW}Verifying AI Brain...{Style.RESET_ALL}")
    from core.ai_brain import get_brain
    try:
        brain = get_brain()
        print_result("AI Provider", True, f"Type: {brain.__class__.__name__}")
    except Exception as e:
        print_result("AI Provider", False, str(e))
        
    # 5. Summary
    print(f"\n{Fore.CYAN}=================================={Style.RESET_ALL}")
    print(f"Run {Fore.GREEN}'python jarvis.py'{Style.RESET_ALL} to start the full system.\n")

if __name__ == "__main__":
    run_diagnostics()
