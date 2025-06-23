from sheets import get_company_data, validate_worksheets
from messaging import send_email, test_email_connection
import time

SHEET_URL = "https://docs.google.com/spreadsheets/d/1nP2VZUqbPPPHB3_cd7c8JBQXEAVoUMSUzNnQ5PvyBkk/edit?gid=1413023431"

# Define the worksheets to process in order
WORKSHEETS = [
    "Plumbing",
    "A/C", 
    # Add more worksheets as needed
]

# Email campaign settings
EMAIL_DELAY = 2  # Delay between emails in seconds
MAX_EMAILS_PER_RUN = 10  # Limit emails per run for testing

def get_email_address(company_info):
    """
    Get email address from company info, checking multiple possible field names.
    """
    # Check different possible email field names
    email_fields = ['e-mail address', 'email', 'e-mail', 'email_address']
    
    for field in email_fields:
        email = company_info.get(field, '')
        if email and '@' in email:
            return email
    
    return ''

def create_email_message(company_info):
    """
    Create a personalized email message for a company.
    """
    company_name = company_info.get('name', 'Your Business')
    
    message = f"""Dear {company_name},

I hope this email finds you well. I'm reaching out because I noticed your business could benefit from professional web development and SEO services.

At JohnsonWebCo, we specialize in:
• Custom website development
• Search engine optimization (SEO)
• E-commerce solutions
• Mobile-responsive design
• Digital marketing strategies

We've helped many businesses like yours increase their online presence and generate more leads.

Would you be interested in a brief 15-minute consultation to discuss how we can help grow your business online?

Best regards,
JohnsonWebCo Team
"""
    
    return message

def process_worksheet(sheet_url, worksheet_name):
    """
    Process a single worksheet and return the data.
    """
    print(f"\n{'='*50}")
    print(f"Processing worksheet: {worksheet_name}")
    print(f"{'='*50}")
    
    try:
        data = get_company_data(sheet_url, worksheet_name)
        print(f"Found {len(data)} companies in {worksheet_name}")
        
        if data:
            print("Sample data:")
            for i, row in enumerate(data[:3]):  # Show first 3 rows as sample
                print(f"  {i+1}. {row}")
            if len(data) > 3:
                print(f"  ... and {len(data) - 3} more companies")
        else:
            print("No data found in this worksheet")
            
        return data
    except Exception as e:
        print(f"Error processing worksheet '{worksheet_name}': {str(e)}")
        return []

def send_campaign_emails(all_data):
    """
    Send email campaign to companies with valid email addresses.
    """
    print(f"\n{'='*50}")
    print("STARTING EMAIL CAMPAIGN")
    print(f"{'='*50}")
    
    # Test email connection first
    if not test_email_connection():
        print("❌ Email connection failed. Cannot proceed with campaign.")
        return
    
    total_sent = 0
    total_skipped = 0
    
    for worksheet_name, companies in all_data.items():
        print(f"\n📧 Processing {worksheet_name} companies...")
        
        for i, company in enumerate(companies):
            if total_sent >= MAX_EMAILS_PER_RUN:
                print(f"\n⚠️  Reached maximum emails per run ({MAX_EMAILS_PER_RUN}). Stopping.")
                break
                
            # Check if company has valid email using the new function
            email = get_email_address(company)
            if not email:
                print(f"⏭️  Skipping {company.get('name', 'Unknown')} - no valid email")
                total_skipped += 1
                continue
            
            # Create and send email
            message = create_email_message(company)
            subject = f"Web Development & SEO Services for {company.get('name', 'Your Business')}"
            
            print(f"📤 Sending email {total_sent + 1}/{MAX_EMAILS_PER_RUN} to {company.get('name', 'Unknown')}...")
            
            if send_email(company, message, subject):
                total_sent += 1
                print(f"✅ Email sent successfully to {company.get('name', 'Unknown')}")
            else:
                total_skipped += 1
                print(f"❌ Failed to send email to {company.get('name', 'Unknown')}")
            
            # Add delay between emails to avoid rate limiting
            if total_sent < MAX_EMAILS_PER_RUN:
                print(f"⏳ Waiting {EMAIL_DELAY} seconds before next email...")
                time.sleep(EMAIL_DELAY)
    
    # Campaign summary
    print(f"\n{'='*50}")
    print("CAMPAIGN SUMMARY")
    print(f"{'='*50}")
    print(f"✅ Emails sent successfully: {total_sent}")
    print(f"⏭️  Companies skipped: {total_skipped}")
    print(f"📊 Total processed: {total_sent + total_skipped}")

def main():
    print("Lead Automation Project - Multi-Sheet Email Campaign")
    print(f"Target worksheets: {', '.join(WORKSHEETS)}")
    print(f"Max emails per run: {MAX_EMAILS_PER_RUN}")
    print(f"Delay between emails: {EMAIL_DELAY} seconds")
    
    # Validate worksheets first
    print("\nValidating worksheets...")
    valid_worksheets, missing_worksheets = validate_worksheets(SHEET_URL, WORKSHEETS)
    
    if missing_worksheets:
        print(f"⚠️  Warning: The following worksheets were not found: {', '.join(missing_worksheets)}")
        print("Only existing worksheets will be processed.")
    
    if not valid_worksheets:
        print("❌ No valid worksheets found. Please check your worksheet names.")
        return {}
    
    print(f"✅ Found {len(valid_worksheets)} valid worksheets: {', '.join(valid_worksheets)}")
    print(f"\nProcessing {len(valid_worksheets)} worksheets sequentially...")
    
    all_data = {}
    
    for worksheet_name in valid_worksheets:
        data = process_worksheet(SHEET_URL, worksheet_name)
        all_data[worksheet_name] = data
        
        # Optional: Add a small delay between worksheets
        time.sleep(1)
    
    # Summary of data found
    print(f"\n{'='*50}")
    print("DATA SUMMARY")
    print(f"{'='*50}")
    total_companies = 0
    for worksheet_name, data in all_data.items():
        count = len(data)
        total_companies += count
        print(f"{worksheet_name}: {count} companies")
    
    print(f"\nTotal companies across all worksheets: {total_companies}")
    
    # Ask user if they want to proceed with email campaign
    if total_companies > 0:
        print(f"\n{'='*50}")
        response = input("Do you want to proceed with the email campaign? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            send_campaign_emails(all_data)
        else:
            print("Email campaign cancelled.")
    else:
        print("No companies found. Cannot proceed with email campaign.")
    
    return all_data

if __name__ == "__main__":
    main() 