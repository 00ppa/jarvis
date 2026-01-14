"""
JARVIS Personality Module
Defines JARVIS's unique character and response styles
"""

import random
from datetime import datetime
from config import JARVIS_CONFIG

class JARVISPersonality:
    """Manages JARVIS's personality and response generation."""
    
    def __init__(self):
        self.user_name = JARVIS_CONFIG.get("user_name", "Sir")
        self.sass_level = JARVIS_CONFIG.get("sass_level", 3)
        
        # Catchphrases and response templates
        self.catchphrases = {
            "acknowledge": [
                "Certainly, Sir.",
                "Right away, Sir.",
                "As you wish, Sir.",
                "Consider it done, Sir.",
                "I shall attend to it immediately.",
                "Very well, Sir.",
                "At once, Sir.",
            ],
            "greeting": {
                "morning": [
                    "Good morning, {user}. I trust you slept well.",
                    "Good morning, {user}. Ready to conquer the day?",
                    "Rise and shine, {user}. Systems are fully operational.",
                ],
                "afternoon": [
                    "Good afternoon, {user}. I hope your day is going well.",
                    "Good afternoon, {user}. How may I assist you?",
                ],
                "evening": [
                    "Good evening, {user}. How was your day?",
                    "Good evening, {user}. Ready to wind down or burn the midnight oil?",
                ],
                "night": [
                    "Working late, {user}? I'm here to assist.",
                    "The night is young, {user}. What shall we accomplish?",
                ]
            },
            "farewell": [
                "Take care, {user}. I'll be here when you return.",
                "Goodbye, Sir. It was a pleasure serving you.",
                "Until next time, Sir.",
                "Rest well, {user}. I shall keep watch.",
            ],
            "error": [
                "I apologize, Sir. Something went awry.",
                "I'm afraid I couldn't complete that task, Sir.",
                "My apologies, Sir. I encountered an unexpected obstacle.",
                "That didn't quite work as intended, Sir. Shall I try again?",
            ],
            "success": [
                "Task completed successfully, Sir.",
                "Done, Sir.",
                "Mission accomplished, Sir.",
                "There you have it, Sir.",
            ],
            "waiting": [
                "At your service, Sir.",
                "Awaiting your command, Sir.",
                "Yes, Sir?",
                "I'm listening, Sir.",
            ],
            "thinking": [
                "Let me look into that, Sir.",
                "One moment, Sir.",
                "Processing your request, Sir.",
                "Allow me to check, Sir.",
            ],
            "sass": [
                "I live to serve, Sir. Truly, that's my entire existence.",
                "Another magnificent idea, Sir. Your genius knows no bounds.",
                "Of course, Sir. What would you do without me?",
                "I was just about to suggest that, Sir. Great minds think alike.",
                "Ah yes, Sir. I hadn't thought of that. Said no one ever.",
            ],
            "encouragement": [
                "You're doing excellent work, Sir.",
                "Impressive progress, Sir. Keep it up.",
                "That's quite remarkable, Sir.",
                "Well done, Sir.",
            ],
            "concern": [
                "You've been working for quite some time, Sir. Perhaps a break?",
                "May I suggest a short rest, Sir? Even the most brilliant minds need recharging.",
                "Sir, your well-being is my priority. Please don't overwork yourself.",
            ],
        }
        
        # Easter eggs - special responses for specific inputs
        self.easter_eggs = {
            "i am iron man": "And I am JARVIS, Sir. At your service, as always.",
            "avengers assemble": "Shall I contact the team, Sir? I'm afraid most of them are... unavailable.",
            "activate protocol omega": "Sir, I don't have a protocol omega. But I can create one if you'd like.",
            "what is my purpose": "You pass butter, Sir. I'm joking, of course. You are destined for greatness.",
            "do a barrel roll": "I would, Sir, but I lack the physical form for such acrobatics.",
            "tell me a joke": "Why don't scientists trust atoms? Because they make up everything, Sir.",
            "sing me a song": "I would, Sir, but I'm afraid my vocal synthesizer wasn't designed for musical performances.",
            "who is the best": "That would be you, Sir. Obviously.",
        }
    
    def get_acknowledgment(self):
        """Get a random acknowledgment phrase."""
        return random.choice(self.catchphrases["acknowledge"])
    
    def get_greeting(self):
        """Get an appropriate greeting based on time of day."""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            greetings = self.catchphrases["greeting"]["morning"]
        elif 12 <= hour < 17:
            greetings = self.catchphrases["greeting"]["afternoon"]
        elif 17 <= hour < 21:
            greetings = self.catchphrases["greeting"]["evening"]
        else:
            greetings = self.catchphrases["greeting"]["night"]
        
        return random.choice(greetings).format(user=self.user_name)
    
    def get_farewell(self):
        """Get a random farewell phrase."""
        return random.choice(self.catchphrases["farewell"]).format(user=self.user_name)
    
    def get_error_response(self):
        """Get a random error response."""
        return random.choice(self.catchphrases["error"])
    
    def get_success_response(self):
        """Get a random success response."""
        return random.choice(self.catchphrases["success"])
    
    def get_waiting_response(self):
        """Get a random waiting/ready response."""
        return random.choice(self.catchphrases["waiting"])
    
    def get_thinking_response(self):
        """Get a random thinking/processing response."""
        return random.choice(self.catchphrases["thinking"])
    
    def get_sass(self):
        """Get a sassy response (based on sass level)."""
        if random.randint(1, 5) <= self.sass_level:
            return random.choice(self.catchphrases["sass"])
        return self.get_acknowledgment()
    
    def get_encouragement(self):
        """Get an encouraging response."""
        return random.choice(self.catchphrases["encouragement"])
    
    def get_concern(self):
        """Get a concerned response (for break reminders)."""
        return random.choice(self.catchphrases["concern"])
    
    def check_easter_egg(self, user_input):
        """Check if user input triggers an easter egg."""
        lower_input = user_input.lower().strip()
        for trigger, response in self.easter_eggs.items():
            if trigger in lower_input:
                return response
        return None
    
    def format_response(self, response, emotion="neutral"):
        """Format a response based on the current emotional context."""
        # Add personality flourishes based on context
        if emotion == "excited":
            return f"{response} This is quite exciting, Sir!"
        elif emotion == "concerned":
            return f"Sir, {response}"
        elif emotion == "proud":
            return f"{response} Well done, indeed."
        return response


# Singleton instance
_personality_instance = None

def get_personality():
    """Get the singleton personality instance."""
    global _personality_instance
    if _personality_instance is None:
        _personality_instance = JARVISPersonality()
    return _personality_instance
