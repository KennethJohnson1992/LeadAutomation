#!/usr/bin/env python3
"""
Debug script to examine worksheet data structure and email field names
"""

from sheets import get_company_data, validate_worksheets

SHEET_URL = "https://docs.google.com/spreadsheets/d/1nP2VZUqbPPPHB3_cd7c8JBQXEAVoUMSUzNnQ5PvyBkk/edit?gid=1413023431"

def debug_worksheet_data(worksheet_name):
    """
    Debug the data structure of a specific worksheet.
    """
    print(f"\n{'='*60}")
    print(f"DEBUGGING WORKSHEET: {worksheet_name}")
    print(f"{'='*60}")
    
    try:
        data = get_company_data(SHEET_URL, worksheet_name)
        print(f"Total rows found: {len(data)}")
        
        if data:
            # Show first 5 rows with all fields
            print(f"\nFirst 5 rows with all fields:")
            for i, row in enumerate(data[:5]):
                print(f"\nRow {i+1}:")
                for key, value in row.items():
                    print(f"  {key}: {value}")
            
            # Check for email-related fields
            print(f"\nEmail field analysis:")
            email_fields = []
            for key in data[0].keys():
                if 'email' in key.lower() or 'mail' in key.lower():
                    email_fields.append(key)
            
            if email_fields:
                print(f"Found email-related fields: {email_fields}")
                
                # Count companies with valid emails
                valid_emails = 0
                for row in data:
                    for field in email_fields:
                        email = row.get(field, '')
                        if email and '@' in email:
                            valid_emails += 1
                            break
                
                print(f"Companies with valid emails: {valid_emails}")
                
                # Show first few companies with emails
                print(f"\nFirst 3 companies with valid emails:")
                count = 0
                for row in data:
                    if count >= 3:
                        break
                    for field in email_fields:
                        email = row.get(field, '')
                        if email and '@' in email:
                            print(f"  {row.get('name', 'Unknown')}: {email}")
                            count += 1
                            break
            else:
                print("No email-related fields found!")
                print("Available fields:", list(data[0].keys()))
        else:
            print("No data found in worksheet")
            
    except Exception as e:
        print(f"Error processing worksheet '{worksheet_name}': {str(e)}")

def main():
    print("WORKSHEET DATA STRUCTURE DEBUG")
    
    worksheets = ["Plumbing", "A/C"]
    
    for worksheet in worksheets:
        debug_worksheet_data(worksheet)

if __name__ == "__main__":
    main() 