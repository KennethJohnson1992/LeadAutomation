#!/usr/bin/env python3
"""
Debug script to check environment variable loading
"""

import os
from dotenv import load_dotenv

def main():
    print("=" * 60)
    print("ENVIRONMENT VARIABLE DEBUG")
    print("=" * 60)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        return
    
    # Load environment variables
    print("\nLoading .env file...")
    load_dotenv()
    
    # Check each environment variable
    env_vars = [
        'SENDER_EMAIL',
        'SENDER_PASSWORD', 
        'SENDER_NAME',
        'SMTP_SERVER',
        'SMTP_PORT',
        'USE_TLS'
    ]
    
    print("\nEnvironment Variables:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            if 'PASSWORD' in var:
                # Mask password for security
                masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '****'
                print(f"  {var}: {masked_value}")
            else:
                print(f"  {var}: {value}")
        else:
            print(f"  {var}: ❌ NOT FOUND")
    
    # Test direct file reading
    print("\nDirect .env file contents:")
    try:
        with open('.env', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if 'PASSWORD' in line:
                        # Mask password in output
                        parts = line.split('=', 1)
                        if len(parts) == 2:
                            password = parts[1]
                            masked_password = password[:4] + '*' * (len(password) - 8) + password[-4:] if len(password) > 8 else '****'
                            print(f"  {parts[0]}={masked_password}")
                    else:
                        print(f"  {line}")
    except Exception as e:
        print(f"  Error reading .env file: {e}")

if __name__ == "__main__":
    main() 