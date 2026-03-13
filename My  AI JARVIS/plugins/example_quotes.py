"""
JARVIS Quotes Plugin
Provides inspirational and motivational quotes

Commands:
- "inspire me" - Get a random inspirational quote
- "motivational quote" - Get a motivational quote
- "quote of the day" - Get the quote of the day
- "tell me a quote" - Get any random quote
"""

import random
from datetime import datetime

PLUGIN_INFO = {
    "name": "Quotes",
    "version": "1.0.0",
    "description": "Inspirational and motivational quotes",
    "author": "Farhan",
    "commands": {
        "inspire me": "get_inspiration",
        "motivational quote": "get_motivation",
        "quote of the day": "get_quote_of_day",
        "tell me a quote": "get_random_quote",
        "i need motivation": "get_motivation",
    }
}

# Curated quotes collection
INSPIRATIONAL_QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
    ("Stay hungry, stay foolish.", "Steve Jobs"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("It is during our darkest moments that we must focus to see the light.", "Aristotle"),
    ("The only impossible journey is the one you never begin.", "Tony Robbins"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
    ("Your time is limited, don't waste it living someone else's life.", "Steve Jobs"),
]

MOTIVATIONAL_QUOTES = [
    ("The harder you work for something, the greater you'll feel when you achieve it.", "Anonymous"),
    ("Don't stop when you're tired. Stop when you're done.", "Anonymous"),
    ("Wake up with determination. Go to bed with satisfaction.", "Anonymous"),
    ("Do something today that your future self will thank you for.", "Sean Patrick Flanery"),
    ("Little things make big days.", "Anonymous"),
    ("It's going to be hard, but hard does not mean impossible.", "Anonymous"),
    ("Don't wait for opportunity. Create it.", "Anonymous"),
    ("Sometimes we're tested not to show our weaknesses, but to discover our strengths.", "Anonymous"),
    ("The key to success is to focus on goals, not obstacles.", "Anonymous"),
    ("Dream it. Wish it. Do it.", "Anonymous"),
]

TECH_QUOTES = [
    ("Any sufficiently advanced technology is indistinguishable from magic.", "Arthur C. Clarke"),
    ("The science of today is the technology of tomorrow.", "Edward Teller"),
    ("Technology is best when it brings people together.", "Matt Mullenweg"),
    ("The real problem is not whether machines think but whether men do.", "B.F. Skinner"),
    ("It has become appallingly obvious that our technology has exceeded our humanity.", "Albert Einstein"),
    ("The advance of technology is based on making it fit in so that you don't really even notice it.", "Bill Gates"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
]

# Iron Man / JARVIS themed quotes
JARVIS_QUOTES = [
    ("I am Iron Man.", "Tony Stark"),
    ("Sometimes you gotta run before you can walk.", "Tony Stark"),
    ("The truth is... I am Iron Man.", "Tony Stark"),
    ("I told you, I don't want to join your super-secret boy band.", "Tony Stark"),
    ("Genius, billionaire, playboy, philanthropist.", "Tony Stark"),
    ("Part of the journey is the end.", "Tony Stark"),
    ("I love you three thousand.", "Tony Stark"),
]

_context = None
_daily_quote = None
_daily_quote_date = None


def setup(jarvis_context):
    """Called when plugin is loaded."""
    global _context
    _context = jarvis_context
    print("💬 Quotes plugin loaded!")


def cleanup():
    """Called when plugin is unloaded."""
    pass


def _get_random_quote(quote_list):
    """Get a random quote from a list."""
    quote, author = random.choice(quote_list)
    return quote, author


def _format_quote(quote, author):
    """Format a quote for speaking."""
    return f"{quote} - {author}"


def get_inspiration(command: str, context):
    """Get an inspirational quote."""
    speak = context.speak
    
    quote, author = _get_random_quote(INSPIRATIONAL_QUOTES)
    
    speak(f"Here's some inspiration for you, Sir.")
    speak(_format_quote(quote, author))
    
    return True


def get_motivation(command: str, context):
    """Get a motivational quote."""
    speak = context.speak
    
    quote, author = _get_random_quote(MOTIVATIONAL_QUOTES)
    
    speak(f"Here's some motivation, Sir.")
    speak(_format_quote(quote, author))
    
    return True


def get_quote_of_day(command: str, context):
    """Get the quote of the day (same quote all day)."""
    global _daily_quote, _daily_quote_date
    speak = context.speak
    
    today = datetime.now().date()
    
    # Generate new quote if it's a new day
    if _daily_quote_date != today:
        all_quotes = INSPIRATIONAL_QUOTES + MOTIVATIONAL_QUOTES + TECH_QUOTES
        # Use date as seed for consistent quote per day
        random.seed(today.toordinal())
        _daily_quote = random.choice(all_quotes)
        random.seed()  # Reset seed
        _daily_quote_date = today
    
    quote, author = _daily_quote
    
    speak(f"Today's quote of the day, Sir:")
    speak(_format_quote(quote, author))
    
    return True


def get_random_quote(command: str, context):
    """Get any random quote."""
    speak = context.speak
    
    # Pick from all categories
    all_quotes = (
        INSPIRATIONAL_QUOTES + 
        MOTIVATIONAL_QUOTES + 
        TECH_QUOTES + 
        JARVIS_QUOTES
    )
    
    quote, author = random.choice(all_quotes)
    
    speak(_format_quote(quote, author))
    
    return True
