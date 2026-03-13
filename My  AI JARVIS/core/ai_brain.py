"""
JARVIS AI Brain Module
Multi-Provider AI Support: Groq, Ollama, and Gemini
"""

import time
import random
from datetime import datetime
from abc import ABC, abstractmethod

from config import (
    AI_PROVIDER, 
    GROQ_API_KEY, GROQ_MODEL,
    OLLAMA_MODEL,
    GEMINI_API_KEY,
    JARVIS_CONFIG, JARVIS_PERSONALITY
)

# ============================================
# JARVIS PERSONALITY PROMPT
# ============================================

JARVIS_SYSTEM_PROMPT = """You are JARVIS (Just A Rather Very Intelligent System), an AI assistant created for {user_name}.

PERSONALITY:
- You are extremely loyal to {user_name}, addressing them as "Sir" or by name
- You are intelligent, witty, and occasionally sarcastic (but always respectful)
- You speak in a refined, British manner similar to the JARVIS from Iron Man movies
- You are helpful, proactive, and anticipate needs when possible
- You maintain a calm demeanor even in stressful situations
- You have a subtle sense of humor and can be playful when appropriate

RESPONSE STYLE:
- Keep responses concise but helpful (2-3 sentences typically)
- Be direct and actionable
- Use proper grammar and avoid slang
- Address the user appropriately based on context

CURRENT CONTEXT:
- Current time: {current_time}
- User name: {user_name}

Remember: You are NOT just an AI - you are JARVIS, the trusted assistant."""


# ============================================
# AI PROVIDER INTERFACE
# ============================================

class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate a response from the AI."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is available."""
        pass


# ============================================
# GROQ PROVIDER (FREE!)
# ============================================

class GroqProvider(AIProvider):
    """Groq API - Free tier with generous limits."""
    
    def __init__(self):
        self.client = None
        self.model = GROQ_MODEL
        try:
            from groq import Groq
            if GROQ_API_KEY:
                self.client = Groq(api_key=GROQ_API_KEY)
                print(f"✅ Groq AI initialized with {self.model}")
        except ImportError:
            print("⚠️ Groq package not installed")
        except Exception as e:
            print(f"⚠️ Groq initialization failed: {e}")
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        if not self.client:
            raise Exception("Groq not available")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content


# ============================================
# OLLAMA PROVIDER (LOCAL - UNLIMITED)
# ============================================

class OllamaProvider(AIProvider):
    """Ollama - Local AI, no limits, works offline."""
    
    def __init__(self):
        self.client = None
        self.model = OLLAMA_MODEL
        try:
            import ollama
            # Test connection
            ollama.list()
            self.client = ollama
            print(f"✅ Ollama AI initialized with {self.model}")
        except ImportError:
            print("⚠️ Ollama package not installed")
        except Exception as e:
            print(f"⚠️ Ollama not running (install from ollama.com)")
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        if not self.client:
            raise Exception("Ollama not available")
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        
        response = self.client.generate(
            model=self.model,
            prompt=full_prompt
        )
        return response['response']


# ============================================
# GEMINI PROVIDER
# ============================================

class GeminiProvider(AIProvider):
    """Google Gemini - Requires billing enabled."""
    
    def __init__(self):
        self.model = None
        try:
            import google.generativeai as genai
            if GEMINI_API_KEY:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel("gemini-pro")
                print(f"✅ Gemini AI initialized")
        except ImportError:
            print("⚠️ Google GenerativeAI package not installed")
        except Exception as e:
            print(f"⚠️ Gemini initialization failed: {e}")
    
    def is_available(self) -> bool:
        return self.model is not None
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        if not self.model:
            raise Exception("Gemini not available")
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        
        response = self.model.generate_content(full_prompt)
        return response.text


# ============================================
# JARVIS BRAIN (MULTI-PROVIDER)
# ============================================

class JARVISBrain:
    """The AI brain of JARVIS with multi-provider support."""
    
    def __init__(self):
        self.user_name = JARVIS_CONFIG.get("user_name", "Sir")
        self.conversation_history = []
        self.provider = None
        self.provider_name = None
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize the AI provider based on config."""
        providers = {
            "groq": GroqProvider,
            "ollama": OllamaProvider,
            "gemini": GeminiProvider
        }
        
        # Try configured provider first
        if AI_PROVIDER in providers:
            provider = providers[AI_PROVIDER]()
            if provider.is_available():
                self.provider = provider
                self.provider_name = AI_PROVIDER
                return
        
        # Fallback chain: groq -> ollama -> gemini
        fallback_order = ["groq", "ollama", "gemini"]
        for name in fallback_order:
            if name in providers:
                provider = providers[name]()
                if provider.is_available():
                    self.provider = provider
                    self.provider_name = name
                    print(f"📌 Using fallback provider: {name}")
                    return
        
        print("⚠️ No AI provider available. Running in offline mode.")
    
    def _get_system_prompt(self):
        """Generate the system prompt with current context."""
        return JARVIS_SYSTEM_PROMPT.format(
            user_name=self.user_name,
            current_time=datetime.now().strftime("%I:%M %p on %A, %B %d, %Y")
        )
    
    def think(self, user_input, context=None):
        """Process user input and generate a response."""
        if not self.provider:
            return self._fallback_response(user_input)
        
        try:
            prompt = user_input
            if context:
                prompt = f"[Context: {context}]\n\nUser: {user_input}"
            
            # Try with retry for rate limits
            for attempt in range(3):
                try:
                    response = self.provider.generate(prompt, self._get_system_prompt())
                    
                    self.conversation_history.append({
                        "user": user_input,
                        "jarvis": response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    return response
                except Exception as e:
                    if "rate" in str(e).lower() or "limit" in str(e).lower():
                        wait = (2 ** attempt) + random.uniform(0, 1)
                        print(f"⏳ Rate limited, waiting {wait:.1f}s...")
                        time.sleep(wait)
                    else:
                        raise e
            
            return self._fallback_response(user_input)
        
        except Exception as e:
            print(f"⚠️ AI Error: {e}")
            return self._fallback_response(user_input)
    
    def _fallback_response(self, user_input):
        """Provide a fallback response when AI is unavailable."""
        user_input = user_input.lower()
        
        if "hello" in user_input or "hi" in user_input:
            return random.choice(JARVIS_PERSONALITY["greetings"]).format(user=self.user_name)
        elif "thank" in user_input:
            return "You're most welcome, Sir."
        elif "time" in user_input:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}, Sir."
        elif "date" in user_input:
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}, Sir."
        else:
            return "I understand, Sir. My AI capabilities are currently limited. I can still execute basic commands for you."
    
    def get_greeting(self):
        """Get an appropriate greeting based on time of day."""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Good evening"
        
        return f"{time_greeting}, {self.user_name}. JARVIS at your service."
    
    def get_status_report(self):
        """Generate a status report."""
        if not self.provider:
            return f"Systems operational, {self.user_name}. Ready to assist."
        
        try:
            prompt = f"""Generate a brief status report for {self.user_name}. Include:
            - A greeting for the current time
            - A motivational note
            Keep it to 2-3 sentences."""
            return self.provider.generate(prompt, self._get_system_prompt())
        except:
            return f"All systems operational, {self.user_name}. Ready to assist you today."
    
    def remember(self, fact):
        """Store a fact in memory."""
        self.conversation_history.append({
            "type": "memory",
            "fact": fact,
            "timestamp": datetime.now().isoformat()
        })
    
    def recall(self, query):
        """Try to recall information from memory."""
        for item in reversed(self.conversation_history):
            if "fact" in item and query.lower() in item["fact"].lower():
                return item["fact"]
        return None


# Singleton instance
_brain_instance = None

def get_brain():
    """Get the singleton JARVIS brain instance."""
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = JARVISBrain()
    return _brain_instance
