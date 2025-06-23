from sheets import get_company_data, validate_worksheets

SHEET_URL = "https://docs.google.com/spreadsheets/d/1nP2VZUqbPPPHB3_cd7c8JBQXEAVoUMSUzNnQ5PvyBkk/edit?gid=1413023431"

# Define the worksheets to process in order
WORKSHEETS = [
    "Plumbing",
    "A/C", 

    # Add more worksheets as needed
]

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

def main():
    print("Lead Automation Project - Multi-Sheet Processing")
    print(f"Target worksheets: {', '.join(WORKSHEETS)}")
    
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
        import time
        time.sleep(1)
    
    # Summary
    print(f"\n{'='*50}")
    print("PROCESSING SUMMARY")
    print(f"{'='*50}")
    total_companies = 0
    for worksheet_name, data in all_data.items():
        count = len(data)
        total_companies += count
        print(f"{worksheet_name}: {count} companies")
    
    print(f"\nTotal companies across all worksheets: {total_companies}")
    
    return all_data

if __name__ == "__main__":
    main() 