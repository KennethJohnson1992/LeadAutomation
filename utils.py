# utils.py
# Helper functions will go here 

def create_env_template():
    """
    Create a template .env file with email configuration.
    """
    env_template = """# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SENDER_NAME=Your Company Name

# Google Sheets Configuration (optional)
GOOGLE_SERVICE_ACCOUNT=service_account.json
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_template)
    
    print("Created .env.template file. Copy it to .env and update with your actual values.")

def validate_email_config():
    """
    Validate that email configuration is properly set up.
    """
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    required_vars = ['SENDER_EMAIL', 'SENDER_PASSWORD', 'SENDER_NAME']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing email configuration variables: {', '.join(missing_vars)}")
        print("Please update your .env file with the required values.")
        return False
    
    print("Email configuration validated successfully.")
    return True 