# messaging.py
# Functions for sending emails and SMS will go here

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Force reload environment variables
load_dotenv(override=True)

# Email configuration - supports both Gmail and Outlook
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER', 'smtp-mail.outlook.com'),  # Outlook default
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),  # Outlook uses 587
    'sender_email': os.getenv('SENDER_EMAIL', 'your-email@outlook.com'),
    'sender_password': os.getenv('SENDER_PASSWORD', 'your-password'),
    'sender_name': os.getenv('SENDER_NAME', 'Your Company Name'),
    'use_tls': os.getenv('USE_TLS', 'True').lower() == 'true'  # Outlook requires TLS
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
        # Validate email address
        recipient_email = company_info.get('e-mail address', '')
        if not recipient_email or '@' not in recipient_email:
            print(f"Skipping {company_info.get('name', 'Unknown')} - no valid email address")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{EMAIL_CONFIG['sender_name']} <{EMAIL_CONFIG['sender_email']}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject or f"Web Development & SEO Services for {company_info.get('name', 'Your Business')}"
        
        # Add message body
        msg.attach(MIMEText(message, 'plain'))
        
        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        
        if EMAIL_CONFIG['use_tls']:
            server.starttls()
        
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], recipient_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {company_info.get('name', 'Unknown')} ({recipient_email})")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {company_info.get('name', 'Unknown')}: {str(e)}")
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

def test_email_connection():
    """
    Test the email connection to verify credentials and settings.
    """
    try:
        print("Testing email connection...")
        print(f"Using email: {EMAIL_CONFIG['sender_email']}")
        print(f"Using server: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")
        
        # Try different authentication methods
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        
        if EMAIL_CONFIG['use_tls']:
            server.starttls()
        
        # Try login with different methods
        try:
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ Authentication failed: {e}")
            print("\nThis error suggests that basic authentication is disabled for your Outlook account.")
            print("You have a few options:")
            print("1. Use a Gmail account instead (easier setup)")
            print("2. Use Microsoft Graph API (requires app registration)")
            print("3. Enable 'Less secure app access' in your Microsoft account (if available)")
            print("4. Use an App Password (if 2FA is enabled)")
            return False
        
        server.quit()
        
        print("✅ Email connection test successful!")
        print(f"   Server: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")
        print(f"   Email: {EMAIL_CONFIG['sender_email']}")
        print(f"   TLS: {EMAIL_CONFIG['use_tls']}")
        return True
        
    except Exception as e:
        print(f"❌ Email connection test failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your email and password in .env file")
        print("2. For Outlook, make sure you're using your regular password (not app password)")
        print("3. Enable 'Less secure app access' in your Outlook account settings")
        print("4. Or use an App Password if you have 2FA enabled")
        print("5. Consider using Gmail instead (easier SMTP setup)")
        return False 