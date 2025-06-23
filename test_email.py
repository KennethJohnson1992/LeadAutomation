#!/usr/bin/env python3
"""
Email Configuration Test Script
Run this to test your Outlook email setup before running the main campaign.
"""

from messaging import test_email_connection, EMAIL_CONFIG
import os
from dotenv import load_dotenv

def main():
    print("=" * 60)
    print("OUTLOOK EMAIL CONFIGURATION TEST")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Display current configuration
    print("\nCurrent Email Configuration:")
    print(f"  SMTP Server: {EMAIL_CONFIG['smtp_server']}")
    print(f"  SMTP Port: {EMAIL_CONFIG['smtp_port']}")
    print(f"  Sender Email: {EMAIL_CONFIG['sender_email']}")
    print(f"  Sender Name: {EMAIL_CONFIG['sender_name']}")
    print(f"  Use TLS: {EMAIL_CONFIG['use_tls']}")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚠️  Warning: No .env file found!")
        print("Please create a .env file with your email credentials.")
        print("You can copy env_template.txt to .env and update the values.")
        return
    
    # Test the connection
    print("\n" + "=" * 60)
    success = test_email_connection()
    
    if success:
        print("\n🎉 Email configuration is working correctly!")
        print("You can now run your email campaign.")
    else:
        print("\n❌ Email configuration needs to be fixed.")
        print("Please check the troubleshooting tips above.")

if __name__ == "__main__":
    main() 