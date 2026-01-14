"""
JARVIS Memory Module
Persistent storage for conversations, preferences, and facts
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from config import DATA_DIR

# Database file
DB_PATH = DATA_DIR / "memory.db"

class JARVISMemory:
    """Persistent memory storage for JARVIS."""
    
    def __init__(self):
        self.db_path = DB_PATH
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_input TEXT NOT NULL,
                jarvis_response TEXT NOT NULL,
                mood TEXT,
                context TEXT
            )
        ''')
        
        # Facts table (things JARVIS should remember)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                category TEXT,
                fact TEXT NOT NULL,
                importance INTEGER DEFAULT 1
            )
        ''')
        
        # Preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                remind_at TEXT NOT NULL,
                message TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            )
        ''')
        
        # Notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                category TEXT DEFAULT 'general'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ============================================
    # CONVERSATION METHODS
    # ============================================
    
    def save_conversation(self, user_input, jarvis_response, mood=None, context=None):
        """Save a conversation exchange."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (timestamp, user_input, jarvis_response, mood, context)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), user_input, jarvis_response, mood, context))
        conn.commit()
        conn.close()
    
    def get_recent_conversations(self, limit=10):
        """Get recent conversations."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, user_input, jarvis_response FROM conversations
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def search_conversations(self, query):
        """Search through past conversations."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, user_input, jarvis_response FROM conversations
            WHERE user_input LIKE ? OR jarvis_response LIKE ?
            ORDER BY id DESC LIMIT 10
        ''', (f'%{query}%', f'%{query}%'))
        results = cursor.fetchall()
        conn.close()
        return results
    
    # ============================================
    # FACTS METHODS
    # ============================================
    
    def remember_fact(self, fact, category="general", importance=1):
        """Store a fact to remember."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO facts (timestamp, category, fact, importance)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), category, fact, importance))
        conn.commit()
        conn.close()
    
    def recall_fact(self, query):
        """Try to recall a fact."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT fact, category FROM facts
            WHERE fact LIKE ?
            ORDER BY importance DESC, id DESC LIMIT 5
        ''', (f'%{query}%',))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_all_facts(self, category=None):
        """Get all stored facts."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if category:
            cursor.execute('SELECT fact, category FROM facts WHERE category = ?', (category,))
        else:
            cursor.execute('SELECT fact, category FROM facts')
        results = cursor.fetchall()
        conn.close()
        return results
    
    # ============================================
    # PREFERENCES METHODS
    # ============================================
    
    def set_preference(self, key, value):
        """Set a user preference."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO preferences (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, json.dumps(value), datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_preference(self, key, default=None):
        """Get a user preference."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM preferences WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return json.loads(result[0])
        return default
    
    # ============================================
    # REMINDERS METHODS
    # ============================================
    
    def add_reminder(self, message, remind_at):
        """Add a reminder."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reminders (created_at, remind_at, message)
            VALUES (?, ?, ?)
        ''', (datetime.now().isoformat(), remind_at, message))
        reminder_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return reminder_id
    
    def get_pending_reminders(self):
        """Get all pending reminders."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute('''
            SELECT id, remind_at, message FROM reminders
            WHERE completed = 0 AND remind_at <= ?
        ''', (now,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def complete_reminder(self, reminder_id):
        """Mark a reminder as completed."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE reminders SET completed = 1 WHERE id = ?', (reminder_id,))
        conn.commit()
        conn.close()
    
    # ============================================
    # NOTES METHODS
    # ============================================
    
    def add_note(self, content, title=None, category="general"):
        """Add a note."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO notes (created_at, title, content, category)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now().isoformat(), title, content, category))
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return note_id
    
    def get_notes(self, category=None, limit=10):
        """Get notes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if category:
            cursor.execute('''
                SELECT id, title, content, created_at FROM notes
                WHERE category = ?
                ORDER BY id DESC LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT id, title, content, created_at FROM notes
                ORDER BY id DESC LIMIT ?
            ''', (limit,))
        results = cursor.fetchall()
        conn.close()
        return results
    
    def search_notes(self, query):
        """Search notes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, content FROM notes
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY id DESC LIMIT 10
        ''', (f'%{query}%', f'%{query}%'))
        results = cursor.fetchall()
        conn.close()
        return results


# Singleton instance
_memory_instance = None

def get_memory():
    """Get the singleton memory instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = JARVISMemory()
    return _memory_instance
