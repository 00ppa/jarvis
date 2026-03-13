"""
JARVIS Productivity Module
Reminders, notes, timers, and daily briefings
"""

import threading
import time
from datetime import datetime, timedelta
import re
from modules.speech_module import speak
from core.memory_module import get_memory
import modules.calendar_module as calendar

class ProductivityManager:
    """Manage reminders, notes, and productivity features."""
    
    def __init__(self):
        self.memory = get_memory()
        self.active_timers = {}
        self.timer_id = 0
    
    # ============================================
    # REMINDERS
    # ============================================
    
    def set_reminder(self, message, time_str):
        """
        Set a reminder.
        
        Args:
            message: What to remind
            time_str: When to remind (e.g., "in 5 minutes", "at 3pm", "tomorrow at 9am")
        
        Returns:
            Reminder ID if successful, None otherwise
        """
        remind_at = self._parse_time(time_str)
        if remind_at:
            reminder_id = self.memory.add_reminder(message, remind_at.isoformat())
            self._schedule_reminder(reminder_id, message, remind_at)
            
            # Sync with Google Calendar
            try:
                cal = calendar.get_calendar_manager()
                cal.add_event(f"Reminder: {message}", remind_at.isoformat())
            except Exception as e:
                print(f"Calendar sync error: {e}")
                
            return reminder_id
        return None
    
    def _parse_time(self, time_str):
        """Parse a natural language time string."""
        time_str = time_str.lower().strip()
        now = datetime.now()
        
        # "in X minutes/hours"
        match = re.search(r'in (\d+) (minute|min|hour|hr)s?', time_str)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            if 'min' in unit:
                return now + timedelta(minutes=amount)
            elif 'hour' in unit or 'hr' in unit:
                return now + timedelta(hours=amount)
        
        # "at X pm/am"
        match = re.search(r'at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?', time_str)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            period = match.group(3)
            
            if period == 'pm' and hour < 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if target <= now:
                target += timedelta(days=1)  # Tomorrow
            return target
        
        # "tomorrow"
        if 'tomorrow' in time_str:
            return now + timedelta(days=1)
        
        return None
    
    def _schedule_reminder(self, reminder_id, message, remind_at):
        """Schedule a reminder to trigger at the specified time."""
        delay = (remind_at - datetime.now()).total_seconds()
        if delay > 0:
            def trigger():
                speak(f"Reminder, Sir: {message}")
                self.memory.complete_reminder(reminder_id)
            
            timer = threading.Timer(delay, trigger)
            timer.daemon = True
            timer.start()
    
    def get_pending_reminders(self):
        """Get all pending reminders."""
        return self.memory.get_pending_reminders()
    
    # ============================================
    # NOTES
    # ============================================
    
    def take_note(self, content, title=None):
        """Save a note."""
        note_id = self.memory.add_note(content, title)
        speak("Note saved, Sir.")
        return note_id
    
    def get_notes(self, limit=5):
        """Get recent notes."""
        return self.memory.get_notes(limit=limit)
    
    def search_notes(self, query):
        """Search through notes."""
        return self.memory.search_notes(query)
    
    def read_last_note(self):
        """Read the most recent note."""
        notes = self.memory.get_notes(limit=1)
        if notes:
            note = notes[0]
            speak(f"Your last note was: {note[2]}")
            return note
        speak("You don't have any notes yet, Sir.")
        return None
    
    # ============================================
    # TIMERS
    # ============================================
    
    def set_timer(self, duration_str, label=None):
        """
        Set a countdown timer.
        
        Args:
            duration_str: Duration (e.g., "5 minutes", "1 hour", "30 seconds")
            label: Optional label for the timer
        """
        seconds = self._parse_duration(duration_str)
        if seconds:
            self.timer_id += 1
            timer_id = self.timer_id
            label = label or f"Timer {timer_id}"
            
            def timer_done():
                speak(f"{label} is complete, Sir!")
                if timer_id in self.active_timers:
                    del self.active_timers[timer_id]
            
            timer = threading.Timer(seconds, timer_done)
            timer.daemon = True
            timer.start()
            
            self.active_timers[timer_id] = {
                "label": label,
                "end_time": datetime.now() + timedelta(seconds=seconds),
                "timer": timer
            }
            
            speak(f"Timer set for {duration_str}, Sir.")
            return timer_id
        
        speak("I couldn't understand that duration, Sir.")
        return None
    
    def _parse_duration(self, duration_str):
        """Parse a duration string to seconds."""
        duration_str = duration_str.lower()
        total_seconds = 0
        
        # Hours
        match = re.search(r'(\d+)\s*(hour|hr)s?', duration_str)
        if match:
            total_seconds += int(match.group(1)) * 3600
        
        # Minutes
        match = re.search(r'(\d+)\s*(minute|min)s?', duration_str)
        if match:
            total_seconds += int(match.group(1)) * 60
        
        # Seconds
        match = re.search(r'(\d+)\s*(second|sec)s?', duration_str)
        if match:
            total_seconds += int(match.group(1))
        
        return total_seconds if total_seconds > 0 else None
    
    def cancel_timer(self, timer_id=None):
        """Cancel a timer."""
        if timer_id and timer_id in self.active_timers:
            timer_obj = self.active_timers[timer_id].get("timer")
            if timer_obj:
                timer_obj.cancel()
            del self.active_timers[timer_id]
            speak("Timer cancelled, Sir.")
            return True
        elif self.active_timers:
            # Cancel the most recent timer
            latest_id = max(self.active_timers.keys())
            timer_obj = self.active_timers[latest_id].get("timer")
            if timer_obj:
                timer_obj.cancel()
            del self.active_timers[latest_id]
            speak("Timer cancelled, Sir.")
            return True
        speak("No active timers to cancel, Sir.")
        return False
    
    def get_active_timers(self):
        """Get all active timers."""
        now = datetime.now()
        active = []
        for tid, info in self.active_timers.items():
            end_time = info.get("end_time")
            if end_time and isinstance(end_time, datetime):
                remaining = (end_time - now).total_seconds()
                if remaining > 0:
                    active.append({
                        "id": tid,
                        "label": info.get("label", "Unknown"),
                        "remaining_seconds": remaining
                    })
        return active
    
    # ============================================
    # TO-DO LIST
    # ============================================
    
    def add_todo(self, task):
        """Add a task to the to-do list."""
        self.memory.remember_fact(task, category="todo", importance=2)
        speak(f"Added to your to-do list: {task}")
    
    def get_todos(self):
        """Get all to-do items."""
        facts = self.memory.get_all_facts(category="todo")
        return [f[0] for f in facts]
    
    def read_todos(self):
        """Read out the to-do list."""
        todos = self.get_todos()
        if todos:
            speak(f"You have {len(todos)} items on your to-do list, Sir.")
            for i, todo in enumerate(todos, 1):
                speak(f"{i}. {todo}")
        else:
            speak("Your to-do list is empty, Sir.")
        return todos


# Singleton instance
_productivity_instance = None

def get_productivity():
    """Get the singleton productivity manager instance."""
    global _productivity_instance
    if _productivity_instance is None:
        _productivity_instance = ProductivityManager()
    return _productivity_instance


# Quick access functions
def remind_me(message, time_str):
    """Quick function to set a reminder."""
    manager = get_productivity()
    result = manager.set_reminder(message, time_str)
    if result:
        speak(f"I'll remind you to {message}, Sir.")
    else:
        speak("I couldn't understand when you want me to remind you, Sir.")
    return result

def take_note(content, title=None):
    """Quick function to take a note."""
    manager = get_productivity()
    return manager.take_note(content, title)

def set_timer(duration_str, label=None):
    """Quick function to set a timer."""
    manager = get_productivity()
    return manager.set_timer(duration_str, label)

def add_todo(task):
    """Quick function to add a to-do item."""
    manager = get_productivity()
    return manager.add_todo(task)
