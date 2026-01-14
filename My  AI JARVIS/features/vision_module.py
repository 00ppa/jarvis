"""
JARVIS Vision Module
Screen awareness and visual analysis using multi-provider AI
"""

import base64
import time
import random
from io import BytesIO
from datetime import datetime
import pyautogui
from PIL import Image

from config import (
    AI_PROVIDER, 
    GROQ_API_KEY, GROQ_MODEL,
    OLLAMA_MODEL,
    GEMINI_API_KEY,
    DATA_DIR
)
from modules.speech_module import speak


class ScreenAwareness:
    """Analyze screen content and provide contextual assistance."""
    
    def __init__(self):
        self.client = None
        self.provider_name = None
        self._initialize_vision()
        self.screenshot_dir = DATA_DIR / "screenshots"
        self.screenshot_dir.mkdir(exist_ok=True)
    
    def _initialize_vision(self):
        """Initialize vision with best available provider."""
        # Groq supports vision with certain models
        if AI_PROVIDER == "groq" or True:  # Try Groq first for vision
            try:
                from groq import Groq
                if GROQ_API_KEY:
                    self.client = Groq(api_key=GROQ_API_KEY)
                    self.provider_name = "groq"
                    self.model = "llama-3.2-90b-vision-preview"  # Vision model
                    print("✅ Vision module initialized with Groq!")
                    return
            except:
                pass
        
        # Fallback to Gemini for vision
        try:
            from google import genai
            if GEMINI_API_KEY:
                self.client = genai.Client(api_key=GEMINI_API_KEY)
                self.provider_name = "gemini"
                self.model = "gemini-2.5-flash"
                print("✅ Vision module initialized with Gemini!")
                return
        except:
            pass
        
        print("⚠️ Vision module: No provider available")
    
    def capture_screen(self, save=False):
        """Capture the current screen."""
        screenshot = pyautogui.screenshot()
        
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.screenshot_dir / f"screen_{timestamp}.png"
            screenshot.save(filepath)
            return screenshot, str(filepath)
        
        return screenshot, None
    
    def _image_to_base64(self, image):
        """Convert PIL Image to base64."""
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def _analyze_with_retry(self, prompt, image, max_retries=3):
        """Analyze image with retry for rate limits."""
        for attempt in range(max_retries):
            try:
                if self.provider_name == "groq":
                    # Groq vision API
                    img_base64 = self._image_to_base64(image)
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                            ]
                        }],
                        max_tokens=500
                    )
                    return response.choices[0].message.content
                
                elif self.provider_name == "gemini":
                    # Gemini vision API
                    buffered = BytesIO()
                    image.save(buffered, format="PNG")
                    image_bytes = buffered.getvalue()
                    
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=[
                            prompt,
                            {"mime_type": "image/png", "data": image_bytes}
                        ]
                    )
                    return response.text
                
            except Exception as e:
                if "rate" in str(e).lower() or "limit" in str(e).lower():
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    print(f"⏳ Rate limited, waiting {wait:.1f}s...")
                    time.sleep(wait)
                else:
                    raise e
        
        raise Exception("Max retries exceeded")
    
    def analyze_screen(self, prompt=None):
        """Analyze the current screen content."""
        if not self.client:
            return "Vision capabilities require an AI provider, Sir."
        
        try:
            screenshot, _ = self.capture_screen()
            
            if not prompt:
                prompt = """Analyze this screenshot and provide a brief summary of:
                1. What application/website is open
                2. What the user appears to be doing
                3. Any notable content or information visible
                Keep the response concise (2-3 sentences)."""
            
            return self._analyze_with_retry(prompt, screenshot)
        
        except Exception as e:
            return f"I couldn't analyze the screen, Sir. Error: {str(e)}"
    
    def describe_screen(self):
        """Give a spoken description of what's on screen."""
        analysis = self.analyze_screen()
        speak(analysis)
        return analysis
    
    def read_text_on_screen(self):
        """Attempt to read and extract text from the screen."""
        if not self.client:
            speak("Vision capabilities require an AI provider, Sir.")
            return None
        
        try:
            screenshot, _ = self.capture_screen()
            
            prompt = """Extract and list all readable text from this screenshot. 
            Focus on the main content, ignoring UI elements like menu bars.
            Format as a clean text summary."""
            
            return self._analyze_with_retry(prompt, screenshot)
        
        except Exception as e:
            return f"Error reading screen: {str(e)}"
    
    def check_for_errors(self):
        """Check if there are any error messages on screen."""
        if not self.client:
            return None
        
        try:
            screenshot, _ = self.capture_screen()
            
            prompt = """Look at this screenshot and identify:
            1. Are there any error messages, warnings, or dialog boxes?
            2. If yes, what do they say?
            3. If it's a code error, what's the likely cause?
            
            If no errors are visible, respond with 'No errors detected.'
            Keep response brief."""
            
            result = self._analyze_with_retry(prompt, screenshot)
            
            if "no error" not in result.lower():
                speak(f"I detected an issue, Sir. {result}")
            
            return result
        
        except Exception as e:
            return f"Error checking screen: {str(e)}"
    
    def help_with_code(self):
        """Provide help if user is looking at code."""
        if not self.client:
            speak("I need an AI provider for code assistance, Sir.")
            return None
        
        try:
            screenshot, _ = self.capture_screen()
            
            prompt = """Analyze this screenshot. If it shows code:
            1. What programming language is it?
            2. What is the code trying to do?
            3. Are there any visible errors or issues?
            4. Suggest an improvement or next step.
            
            If it's not code, briefly describe what's shown instead.
            Keep response concise."""
            
            result = self._analyze_with_retry(prompt, screenshot)
            speak(result)
            return result
        
        except Exception as e:
            speak("I encountered an error analyzing the code, Sir.")
            return None


# Singleton instance
_vision_instance = None

def get_vision():
    """Get the singleton vision instance."""
    global _vision_instance
    if _vision_instance is None:
        _vision_instance = ScreenAwareness()
    return _vision_instance


# Quick access functions
def whats_on_screen():
    """Quick function to describe the screen."""
    vision = get_vision()
    return vision.describe_screen()

def check_errors():
    """Quick function to check for errors on screen."""
    vision = get_vision()
    return vision.check_for_errors()

def help_with_code():
    """Quick function to help with visible code."""
    vision = get_vision()
    return vision.help_with_code()
