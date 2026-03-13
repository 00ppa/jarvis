"""
JARVIS Plugin Loader
Discovers, loads, and manages plugins
"""

import os
import sys
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Any

from config import BASE_DIR


class PluginLoader:
    """
    Discovers and manages JARVIS plugins.
    
    Plugins are Python files in the plugins/ directory that follow
    the plugin interface specification.
    """
    
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = BASE_DIR / plugins_dir
        self.loaded_plugins: Dict[str, Any] = {}  # name -> plugin instance/module
        self.plugin_commands: Dict[str, tuple] = {}  # trigger -> (plugin_name, handler)
        self.disabled_plugins: List[str] = []
        self.context = None
    
    def initialize(self, disabled_plugins: List[str] = None):
        """
        Initialize the plugin loader and discover plugins.
        
        Args:
            disabled_plugins: List of plugin names to skip
        """
        self.disabled_plugins = disabled_plugins or []
        
        # Create plugins directory if it doesn't exist
        self.plugins_dir.mkdir(exist_ok=True)
        
        # Create __init__.py if it doesn't exist
        init_file = self.plugins_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("# JARVIS Plugins Directory\n")
        
        # Create context for plugins
        from core.plugin_base import PluginContext
        self.context = PluginContext.create()
        
        # Discover and load plugins
        self._discover_plugins()
    
    def _discover_plugins(self):
        """Scan plugins directory and load valid plugins."""
        if not self.plugins_dir.exists():
            print("⚠️ Plugins directory not found")
            return
        
        # Add plugins dir to path for imports
        plugins_path = str(self.plugins_dir)
        if plugins_path not in sys.path:
            sys.path.insert(0, plugins_path)
        
        for file in self.plugins_dir.glob("*.py"):
            if file.name.startswith("_"):
                continue  # Skip __init__.py and private files
            
            try:
                self._load_plugin(file)
            except Exception as e:
                print(f"⚠️ Failed to load plugin {file.name}: {e}")
    
    def _load_plugin(self, plugin_path: Path):
        """
        Load a single plugin from file.
        
        Args:
            plugin_path: Path to the plugin Python file
        """
        module_name = plugin_path.stem
        
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, plugin_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot load spec for {plugin_path}")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        # Check for PLUGIN_INFO
        if not hasattr(module, "PLUGIN_INFO"):
            raise ValueError(f"Plugin {module_name} missing PLUGIN_INFO")
        
        plugin_info = module.PLUGIN_INFO
        plugin_name = plugin_info.get("name", module_name)
        
        # Check if disabled
        if plugin_name in self.disabled_plugins:
            print(f"⏸️ Plugin '{plugin_name}' is disabled")
            return
        
        # Call setup if exists
        if hasattr(module, "setup"):
            module.setup(self.context)
        
        # Register commands
        commands = plugin_info.get("commands", {})
        for trigger, handler_name in commands.items():
            if hasattr(module, handler_name):
                handler = getattr(module, handler_name)
                self.plugin_commands[trigger.lower()] = (plugin_name, handler)
        
        # Store plugin
        self.loaded_plugins[plugin_name] = {
            "module": module,
            "info": plugin_info,
            "path": plugin_path,
        }
        
        print(f"✅ Loaded plugin: {plugin_name} v{plugin_info.get('version', '?')}")
    
    def unload_plugin(self, plugin_name: str):
        """
        Unload a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to unload
        """
        if plugin_name not in self.loaded_plugins:
            return False
        
        plugin_data = self.loaded_plugins[plugin_name]
        module = plugin_data["module"]
        
        # Call cleanup if exists
        if hasattr(module, "cleanup"):
            try:
                module.cleanup()
            except Exception as e:
                print(f"⚠️ Error during plugin cleanup: {e}")
        
        # Remove commands
        triggers_to_remove = [
            trigger for trigger, (name, _) in self.plugin_commands.items()
            if name == plugin_name
        ]
        for trigger in triggers_to_remove:
            del self.plugin_commands[trigger]
        
        # Remove from loaded plugins
        del self.loaded_plugins[plugin_name]
        
        print(f"🔌 Unloaded plugin: {plugin_name}")
        return True
    
    def reload_plugins(self):
        """Reload all plugins."""
        # Unload all
        for name in list(self.loaded_plugins.keys()):
            self.unload_plugin(name)
        
        # Reload all
        self._discover_plugins()
        
        return len(self.loaded_plugins)
    
    def handle_command(self, command: str) -> bool:
        """
        Try to handle a command with loaded plugins.
        
        Args:
            command: The user's command
            
        Returns:
            True if a plugin handled the command, False otherwise
        """
        command_lower = command.lower()
        
        # Check each registered trigger
        for trigger, (plugin_name, handler) in self.plugin_commands.items():
            if trigger in command_lower:
                try:
                    result = handler(command, self.context)
                    return result if result is not None else True
                except Exception as e:
                    print(f"⚠️ Plugin error ({plugin_name}): {e}")
                    return False
        
        return False
    
    def get_plugin_list(self) -> List[Dict]:
        """Get list of loaded plugins with their info."""
        return [
            {
                "name": name,
                "version": data["info"].get("version", "?"),
                "description": data["info"].get("description", ""),
                "author": data["info"].get("author", "Unknown"),
                "commands": list(data["info"].get("commands", {}).keys()),
            }
            for name, data in self.loaded_plugins.items()
        ]
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable a disabled plugin."""
        if plugin_name in self.disabled_plugins:
            self.disabled_plugins.remove(plugin_name)
            self.reload_plugins()
            return True
        return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable a plugin."""
        if plugin_name in self.loaded_plugins:
            self.unload_plugin(plugin_name)
            self.disabled_plugins.append(plugin_name)
            return True
        return False


# Singleton instance
_loader_instance: Optional[PluginLoader] = None


def get_plugin_loader() -> PluginLoader:
    """Get the singleton plugin loader instance."""
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = PluginLoader()
    return _loader_instance


def initialize_plugins(disabled_plugins: List[str] = None):
    """Initialize the plugin system."""
    loader = get_plugin_loader()
    loader.initialize(disabled_plugins)
    return loader


def handle_plugin_command(command: str) -> bool:
    """Try to handle a command with plugins."""
    loader = get_plugin_loader()
    return loader.handle_command(command)
