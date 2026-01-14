"""
JARVIS Emotion Module
Detect user mood and adapt responses accordingly
"""

from datetime import datetime
from config import JARVIS_CONFIG

# Simple keyword-based sentiment indicators
MOOD_INDICATORS = {
    "positive": [
        "happy", "great", "awesome", "fantastic", "excellent", "amazing",
        "good", "wonderful", "love", "excited", "thanks", "thank you",
        "perfect", "brilliant", "nice", "cool", "yes"
    ],
    "negative": [
        "sad", "angry", "frustrated", "annoyed", "terrible", "hate",
        "bad", "awful", "horrible", "stressed", "tired", "exhausted",
        "damn", "shit", "fuck", "stupid", "idiot", "ugh"
    ],
    "stressed": [
        "stressed", "overwhelmed", "anxious", "worried", "nervous",
        "deadline", "urgent", "hurry", "help", "can't", "impossible"
    ],
    "tired": [
        "tired", "exhausted", "sleepy", "fatigue", "weary", "drained",
        "long day", "need rest", "can't focus"
    ],
    "curious": [
        "why", "how", "what", "tell me", "explain", "curious",
        "wondering", "interested", "learn"
    ]
}

# Response adaptations for different moods
MOOD_RESPONSES = {
    "positive": {
        "tone": "enthusiastic",
        "prefix": ["Excellent!", "Wonderful!", "That's great to hear, Sir!"],
        "suffix": ["Keep up that energy, Sir!", ""]
    },
    "negative": {
        "tone": "supportive",
        "prefix": ["I understand, Sir.", "I see.", "I'm here to help, Sir."],
        "suffix": ["Let me know how I can assist.", "We'll get through this, Sir."]
    },
    "stressed": {
        "tone": "calm",
        "prefix": ["Take a breath, Sir.", "Let's tackle this together, Sir."],
        "suffix": ["One step at a time, Sir.", "I'm here to help reduce your burden."]
    },
    "tired": {
        "tone": "gentle",
        "prefix": ["Of course, Sir.", "Right away, Sir."],
        "suffix": ["Perhaps consider some rest when you can, Sir.", ""]
    },
    "curious": {
        "tone": "informative",
        "prefix": ["Great question, Sir.", "Allow me to explain, Sir."],
        "suffix": ["Would you like to know more?", ""]
    },
    "neutral": {
        "tone": "professional",
        "prefix": ["Certainly, Sir.", "Of course, Sir."],
        "suffix": ["", "Is there anything else?"]
    }
}


class EmotionDetector:
    """Detect and track user emotional state."""
    
    def __init__(self):
        self.current_mood = "neutral"
        self.mood_history = []
        self.enabled = JARVIS_CONFIG.get("enable_mood_detection", True)
    
    def detect_mood(self, text):
        """
        Detect mood from text input.
        
        Args:
            text: User's spoken/typed input
        
        Returns:
            Detected mood string
        """
        if not self.enabled or not text:
            return self.current_mood
        
        text_lower = text.lower()
        mood_scores = {
            "positive": 0,
            "negative": 0,
            "stressed": 0,
            "tired": 0,
            "curious": 0
        }
        
        # Count mood indicators
        for mood, indicators in MOOD_INDICATORS.items():
            for indicator in indicators:
                if indicator in text_lower:
                    mood_scores[mood] += 1
        
        # Find dominant mood
        max_score = max(mood_scores.values())
        if max_score > 0:
            detected_mood = max(mood_scores, key=mood_scores.get)
        else:
            detected_mood = "neutral"
        
        # Update history
        self.mood_history.append({
            "mood": detected_mood,
            "timestamp": datetime.now().isoformat(),
            "text_snippet": text[:50]
        })
        
        # Keep only last 20 entries
        if len(self.mood_history) > 20:
            self.mood_history = self.mood_history[-20:]
        
        self.current_mood = detected_mood
        return detected_mood
    
    def get_current_mood(self):
        """Get the current detected mood."""
        return self.current_mood
    
    def get_mood_trend(self):
        """Analyze mood trend over recent interactions."""
        if len(self.mood_history) < 3:
            return "unknown"
        
        recent = self.mood_history[-5:]
        moods = [entry["mood"] for entry in recent]
        
        # Count occurrences
        from collections import Counter
        mood_counts = Counter(moods)
        most_common = mood_counts.most_common(1)[0][0]
        
        return most_common
    
    def get_response_adaptation(self):
        """Get response adaptation settings for current mood."""
        return MOOD_RESPONSES.get(self.current_mood, MOOD_RESPONSES["neutral"])
    
    def adapt_response(self, response):
        """
        Adapt a response based on detected mood.
        
        Args:
            response: Original response text
        
        Returns:
            Adapted response with mood-appropriate prefix/suffix
        """
        if not self.enabled:
            return response
        
        adaptation = self.get_response_adaptation()
        
        import random
        prefix = random.choice(adaptation["prefix"]) if adaptation["prefix"] else ""
        suffix = random.choice(adaptation["suffix"]) if adaptation["suffix"] else ""
        
        parts = []
        if prefix:
            parts.append(prefix)
        parts.append(response)
        if suffix:
            parts.append(suffix)
        
        return " ".join(parts)
    
    def should_show_concern(self):
        """Check if JARVIS should express concern about user wellbeing."""
        if len(self.mood_history) < 3:
            return False
        
        recent_moods = [entry["mood"] for entry in self.mood_history[-5:]]
        negative_count = sum(1 for m in recent_moods if m in ["negative", "stressed", "tired"])
        
        return negative_count >= 3
    
    def get_encouragement(self):
        """Get an encouraging message based on mood."""
        if self.current_mood == "stressed":
            return "Remember, Sir, you've overcome challenges before. You've got this."
        elif self.current_mood == "tired":
            return "You're doing great, Sir. Rest when you can - you've earned it."
        elif self.current_mood == "negative":
            return "Things will get better, Sir. I'm here to help however I can."
        else:
            return "You're doing excellent work, Sir."


# Singleton instance
_emotion_instance = None

def get_emotion_detector():
    """Get the singleton emotion detector instance."""
    global _emotion_instance
    if _emotion_instance is None:
        _emotion_instance = EmotionDetector()
    return _emotion_instance


# Quick access functions
def detect_mood(text):
    """Quick function to detect mood from text."""
    detector = get_emotion_detector()
    return detector.detect_mood(text)

def get_encouragement():
    """Quick function to get an encouraging message."""
    detector = get_emotion_detector()
    return detector.get_encouragement()

def adapt_response(response):
    """Quick function to adapt a response to current mood."""
    detector = get_emotion_detector()
    return detector.adapt_response(response)
