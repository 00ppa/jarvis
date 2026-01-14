"""
JARVIS Proactive Engine
Autonomous suggestions and alerts
"""

import threading
import time
from datetime import datetime, timedelta
from modules.speech_module import speak
from modules.system_monitor import get_system_monitor
from core.memory_module import get_memory
from config import JARVIS_CONFIG

class ProactiveEngine:
    """Engine for proactive suggestions and automated alerts."""
    
    def __init__(self):
        self.enabled = JARVIS_CONFIG.get("enable_proactive", True)
        self.running = False
        self.check_thread = None
        self.last_break_reminder = None
        self.work_start_time = None
        self.last_alerts = {}
    
    def start(self):
        """Start the proactive monitoring."""
        if not self.enabled:
            return
        
        self.running = True
        self.work_start_time = datetime.now()
        self.check_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.check_thread.start()
        print("✅ Proactive engine started!")
    
    def stop(self):
        """Stop the proactive monitoring."""
        self.running = False
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.running:
            try:
                self._check_all()
            except Exception as e:
                print(f"Proactive engine error: {e}")
            time.sleep(60)  # Check every minute
    
    def _check_all(self):
        """Run all proactive checks."""
        self._check_system_health()
        self._check_break_reminder()
        self._check_reminders()
    
    def _check_system_health(self):
        """Check system health and alert if needed."""
        monitor = get_system_monitor()
        alerts = monitor.check_alerts()
        
        for alert in alerts:
            alert_key = alert[:20]  # Use first 20 chars as key
            last_alert = self.last_alerts.get(alert_key)
            
            # Only alert if we haven't alerted for this in the last 5 minutes
            if not last_alert or (datetime.now() - last_alert).seconds > 300:
                speak(f"Sir, {alert}")
                self.last_alerts[alert_key] = datetime.now()
    
    def _check_break_reminder(self):
        """Remind user to take breaks."""
        if not self.work_start_time:
            return
        
        work_duration = (datetime.now() - self.work_start_time).seconds / 60  # in minutes
        
        # Remind every 45-60 minutes
        if work_duration >= 45:
            if not self.last_break_reminder:
                speak("Sir, you've been working for 45 minutes. Perhaps a short break would be beneficial?")
                self.last_break_reminder = datetime.now()
            elif (datetime.now() - self.last_break_reminder).seconds > 2700:  # 45 minutes
                speak("Just a gentle reminder, Sir. You've been working for quite a while.")
                self.last_break_reminder = datetime.now()
    
    def _check_reminders(self):
        """Check and trigger pending reminders."""
        memory = get_memory()
        reminders = memory.get_pending_reminders()
        
        for reminder_id, remind_at, message in reminders:
            speak(f"Reminder, Sir: {message}")
            memory.complete_reminder(reminder_id)
    
    def get_morning_briefing(self):
        """Generate a morning briefing."""
        now = datetime.now()
        briefing_parts = []
        
        # Time and date
        briefing_parts.append(f"Good morning, Sir. It's {now.strftime('%I:%M %p')} on {now.strftime('%A, %B %d')}.")
        
        # System status
        monitor = get_system_monitor()
        battery = monitor.get_battery_status()
        if battery:
            if battery['percent'] < 30:
                briefing_parts.append(f"Your battery is at {battery['percent']}%. You may want to plug in.")
            else:
                briefing_parts.append(f"Battery is at {battery['percent']}%.")
        
        # Pending reminders
        memory = get_memory()
        reminders = memory.get_pending_reminders()
        if reminders:
            briefing_parts.append(f"You have {len(reminders)} pending reminders.")
        
        # Todo items
        todos = memory.get_all_facts(category="todo")
        if todos:
            briefing_parts.append(f"You have {len(todos)} items on your to-do list.")
        
        briefing_parts.append("How may I assist you today?")
        
        full_briefing = " ".join(briefing_parts)
        speak(full_briefing)
        return full_briefing
    
    def suggest_action(self):
        """Suggest a proactive action based on context."""
        now = datetime.now()
        hour = now.hour
        
        # Time-based suggestions
        if 6 <= hour < 9:
            return "Perhaps check your emails and plan your day, Sir?"
        elif 12 <= hour < 13:
            return "It's around lunch time, Sir. Remember to eat!"
        elif 17 <= hour < 18:
            return "The workday is winding down, Sir. Time to review your accomplishments?"
        elif 22 <= hour or hour < 6:
            return "It's quite late, Sir. Perhaps you should rest soon?"
        
        return None
    
    def user_took_break(self):
        """Record that the user took a break."""
        self.work_start_time = datetime.now()
        self.last_break_reminder = None
        speak("Enjoy your break, Sir. I'll be here when you return.")


# Singleton instance
_engine_instance = None

def get_proactive_engine():
    """Get the singleton proactive engine instance."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ProactiveEngine()
    return _engine_instance


# Quick access functions
def start_proactive():
    """Start the proactive engine."""
    engine = get_proactive_engine()
    engine.start()

def stop_proactive():
    """Stop the proactive engine."""
    engine = get_proactive_engine()
    engine.stop()

def morning_briefing():
    """Give the morning briefing."""
    engine = get_proactive_engine()
    return engine.get_morning_briefing()

def taking_break():
    """Notify that user is taking a break."""
    engine = get_proactive_engine()
    engine.user_took_break()
