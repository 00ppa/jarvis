"""
JARVIS System Monitor Module
Real-time system monitoring and control
"""

import psutil
import platform
import socket
from datetime import datetime
from modules.speech_module import speak

class SystemMonitor:
    """Monitor and report system status."""
    
    def __init__(self):
        self.system_info = self._get_system_info()
    
    def _get_system_info(self):
        """Get static system information."""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": socket.gethostname(),
        }
    
    # ============================================
    # CPU MONITORING
    # ============================================
    
    def get_cpu_usage(self):
        """Get current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)
    
    def get_cpu_cores(self):
        """Get CPU core count."""
        return psutil.cpu_count(logical=True)
    
    def get_cpu_freq(self):
        """Get CPU frequency in MHz."""
        freq = psutil.cpu_freq()
        if freq:
            return round(freq.current, 2)
        return None
    
    # ============================================
    # MEMORY MONITORING
    # ============================================
    
    def get_memory_usage(self):
        """Get memory usage information."""
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / (1024**3), 2),
            "available_gb": round(memory.available / (1024**3), 2),
            "used_gb": round(memory.used / (1024**3), 2),
            "percent": memory.percent
        }
    
    # ============================================
    # DISK MONITORING
    # ============================================
    
    def get_disk_usage(self, path="C:/"):
        """Get disk usage for a specific path."""
        try:
            disk = psutil.disk_usage(path)
            return {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "percent": round((disk.used / disk.total) * 100, 1)
            }
        except:
            return None
    
    # ============================================
    # BATTERY MONITORING
    # ============================================
    
    def get_battery_status(self):
        """Get battery information."""
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "plugged_in": battery.power_plugged,
                "time_left_mins": battery.secsleft // 60 if battery.secsleft > 0 else None
            }
        return None
    
    # ============================================
    # NETWORK MONITORING
    # ============================================
    
    def get_network_status(self):
        """Get network connection status."""
        try:
            # Check internet connectivity
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            connected = True
        except OSError:
            connected = False
        
        return {
            "connected": connected,
            "hostname": socket.gethostname(),
        }
    
    # ============================================
    # PROCESS MANAGEMENT
    # ============================================
    
    def get_running_processes(self, limit=10):
        """Get top processes by CPU usage."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        return processes[:limit]
    
    def kill_process(self, process_name):
        """Kill a process by name."""
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    proc.kill()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return killed
    
    def is_process_running(self, process_name):
        """Check if a process is running."""
        for proc in psutil.process_iter(['name']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False
    
    # ============================================
    # COMPREHENSIVE REPORTS
    # ============================================
    
    def get_full_status(self):
        """Get a comprehensive system status report."""
        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        disk = self.get_disk_usage()
        battery = self.get_battery_status()
        network = self.get_network_status()
        
        return {
            "cpu_percent": cpu,
            "memory": memory,
            "disk": disk,
            "battery": battery,
            "network": network,
            "timestamp": datetime.now().isoformat()
        }
    
    def speak_status_report(self):
        """Generate and speak a status report."""
        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        battery = self.get_battery_status()
        
        report = f"System status, Sir. CPU is at {cpu}%, "
        report += f"memory at {memory['percent']}% used. "
        
        if battery:
            if battery['plugged_in']:
                report += f"Battery at {battery['percent']}%, charging."
            elif battery['percent'] < 20:
                report += f"Battery critically low at {battery['percent']}%! Please plug in, Sir."
            else:
                report += f"Battery at {battery['percent']}%."
        
        speak(report)
        return report
    
    def check_alerts(self):
        """Check for system alerts and warnings."""
        alerts = []
        
        # CPU alert
        cpu = self.get_cpu_usage()
        if cpu > 90:
            alerts.append(f"High CPU usage detected: {cpu}%")
        
        # Memory alert
        memory = self.get_memory_usage()
        if memory['percent'] > 85:
            alerts.append(f"High memory usage: {memory['percent']}%")
        
        # Disk alert
        disk = self.get_disk_usage()
        if disk and disk['percent'] > 90:
            alerts.append(f"Disk space low: only {disk['free_gb']}GB free")
        
        # Battery alert
        battery = self.get_battery_status()
        if battery and not battery['plugged_in'] and battery['percent'] < 15:
            alerts.append(f"Battery critically low: {battery['percent']}%")
        
        return alerts


# Singleton instance
_monitor_instance = None

def get_system_monitor():
    """Get the singleton system monitor instance."""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = SystemMonitor()
    return _monitor_instance


# Quick access functions
def system_status():
    """Quick function to get and speak system status."""
    monitor = get_system_monitor()
    return monitor.speak_status_report()

def cpu_status():
    """Get CPU status."""
    monitor = get_system_monitor()
    usage = monitor.get_cpu_usage()
    speak(f"CPU usage is at {usage}%, Sir.")
    return usage

def memory_status():
    """Get memory status."""
    monitor = get_system_monitor()
    mem = monitor.get_memory_usage()
    speak(f"Memory usage is at {mem['percent']}%. {mem['available_gb']}GB available out of {mem['total_gb']}GB, Sir.")
    return mem

def battery_status():
    """Get battery status."""
    monitor = get_system_monitor()
    battery = monitor.get_battery_status()
    if battery:
        status = "charging" if battery['plugged_in'] else "on battery"
        speak(f"Battery is at {battery['percent']}%, currently {status}, Sir.")
        return battery
    speak("No battery detected, Sir. You're likely on a desktop.")
    return None

def kill_app(app_name):
    """Kill an application by name."""
    monitor = get_system_monitor()
    if monitor.kill_process(app_name):
        speak(f"I've terminated {app_name}, Sir.")
        return True
    speak(f"I couldn't find {app_name} running, Sir.")
    return False
