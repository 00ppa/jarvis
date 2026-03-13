"""
JARVIS Plugin Base
Base class and interface for JARVIS plugins
"""

from abc import ABC, abstractmethod
from typing import Dict, Callable, Optional, Any


class JARVISPlugin(ABC):
    """
    Base class for JARVIS plugins.
    
    All plugins should inherit from this class and implement
    the required methods and properties.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version (e.g., '1.0.0')."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Brief description of what the plugin does."""
        pass
    
    @property
    def author(self) -> str:
        """Plugin author (optional)."""
        return "Unknown"
    
    @property
    def commands(self) -> Dict[str, Callable]:
        """
        Dictionary mapping trigger phrases to handler functions.
        
        Example:
            {
                "what's the weather": self.get_weather,
                "weather forecast": self.get_forecast,
            }
        """
        return {}
    
    def setup(self, jarvis_context: Any) -> None:
        """
        Called when the plugin is loaded.
        
        Use this for initialization, registering event hooks, etc.
        
        Args:
            jarvis_context: Access to JARVIS modules and config
        """
        pass
    
    def cleanup(self) -> None:
        """
        Called when the plugin is unloaded.
        
        Use this for cleanup, saving state, etc.
        """
        pass
    
    def handle_command(self, trigger: str, full_command: str, context: Any) -> bool:
        """
        Handle a command that matches one of this plugin's triggers.
        
        Args:
            trigger: The matched trigger phrase
            full_command: The full user command
            context: JARVIS context object
            
        Returns:
            True if command was handled, False otherwise
        """
        handler = self.commands.get(trigger)
        if handler:
            handler(full_command, context)
            return True
        return False


class PluginContext:
    """
    Context object passed to plugins providing access to JARVIS functionality.
    """
    
    def __init__(self):
        self.speak = None
        self.listen = None
        self.memory = None
        self.config = None
        self.brain = None
    
    @classmethod
    def create(cls):
        """Create a plugin context with access to JARVIS modules."""
        from modules.speech_module import speak, listen
        from core.memory_module import get_memory
        from core.ai_brain import get_brain
        from config import JARVIS_CONFIG
        
        ctx = cls()
        ctx.speak = speak
        ctx.listen = listen
        ctx.memory = get_memory()
        ctx.config = JARVIS_CONFIG
        ctx.brain = get_brain()
        return ctx
