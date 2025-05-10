import psutil
import smtplib
from email.mime.text import MIMEText
import time
import logging
import os

# Configure logging
logging.basicConfig(filename='server_health.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_system_health():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    return cpu_usage, memory_usage

def send_alert(cpu_usage, memory_usage):
    sender = "your_email@gmail.com"
    recipient = "recipient_email@example.com"
    subject = "Server Health Alert"
    body = f"Warning! The server has exceeded its thresholds.\n\nCPU Usage: {cpu_usage}%\nMemory Usage: {memory_usage}%"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, 'your_password')
            server.sendmail(sender, [recipient], msg.as_string())
        logging.info("Alert sent successfully!")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")

def check_thresholds():
    cpu_usage, memory_usage = get_system_health()
    cpu_threshold = 80
    memory_threshold = 75

    if cpu_usage > cpu_threshold:
        logging.warning(f"CPU usage is high: {cpu_usage}%")
        send_alert(cpu_usage, memory_usage)
    
    if memory_usage > memory_threshold:
        logging.warning(f"Memory usage is high: {memory_usage}%")
        send_alert(cpu_usage, memory_usage)

def monitor():
    while True:
        check_thresholds()
        logging.info(f"CPU: {psutil.cpu_percent()}% | Memory: {psutil.virtual_memory().percent}%")
        time.sleep(300)

if __name__ == '__main__':
    monitor()
