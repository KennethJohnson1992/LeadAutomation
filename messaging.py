# messaging.py
# Functions for sending emails and SMS will go here

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email configuration - easily changeable
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',  # Change for different providers
    'smtp_port': 587,
    'sender_email': os.getenv('SENDER_EMAIL', 'your-email@gmail.com'),
    'sender_password': os.getenv('SENDER_PASSWORD', 'your-app-password'),
    'sender_name': os.getenv('SENDER_NAME', 'Your Company Name')
}

def send_email(company_info, message, subject=None):
    """
    Send email to a company using the configured email settings.
    
    :param company_info: Dictionary containing company data
    :param message: The message content to send
    :param subject: Email subject (optional)
    :return: True if successful, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{EMAIL_CONFIG['sender_name']} <{EMAIL_CONFIG['sender_email']}>"
        msg['To'] = company_info.get('e-mail address', '')
        msg['Subject'] = subject or f"Web Development & SEO Services for {company_info.get('name', 'Your Business')}"
        
        # Add message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], company_info.get('e-mail address', ''), text)
        server.quit()
        
        print(f"Email sent successfully to {company_info.get('name', 'Unknown')}")
        return True
        
    except Exception as e:
        print(f"Failed to send email to {company_info.get('name', 'Unknown')}: {str(e)}")
        return False

def send_sms(company_info, message):
    """
    Placeholder for SMS functionality.
    :param company_info: Dictionary containing company data
    :param message: The message content to send
    :return: True if successful, False otherwise
    """
    # TODO: Implement SMS sending (e.g., using Twilio)
    print(f"SMS functionality not yet implemented for {company_info.get('name', 'Unknown')}")
    return False

def update_email_config(new_config):
    """
    Update email configuration easily.
    :param new_config: Dictionary with new email settings
    """
    global EMAIL_CONFIG
    EMAIL_CONFIG.update(new_config)
    print("Email configuration updated successfully") 