import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Define the scope for Google Sheets and Drive API
SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

# Path to the service account key
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT', 'service_account.json')


def get_company_data(sheet_name, worksheet_name):
    """
    Fetch company data from a Google Sheet.
    :param sheet_name: The name or URL of the Google Sheet
    :param worksheet_name: The name of the worksheet/tab
    :return: List of dictionaries, one per row
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, SCOPE
    )
    client = gspread.authorize(creds)
    if sheet_name.startswith('http'):
        sheet = client.open_by_url(sheet_name)
    else:
        sheet = client.open(sheet_name)
    records = sheet.worksheet(worksheet_name).get_all_records()
    return records

def get_available_worksheets(sheet_name):
    """
    Get all available worksheet names from a Google Sheet.
    :param sheet_name: The name or URL of the Google Sheet
    :return: List of worksheet names
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, SCOPE
    )
    client = gspread.authorize(creds)
    if sheet_name.startswith('http'):
        sheet = client.open_by_url(sheet_name)
    else:
        sheet = client.open(sheet_name)
    
    worksheet_names = [worksheet.title for worksheet in sheet.worksheets()]
    return worksheet_names

def validate_worksheets(sheet_name, target_worksheets):
    """
    Validate that all target worksheets exist in the Google Sheet.
    :param sheet_name: The name or URL of the Google Sheet
    :param target_worksheets: List of worksheet names to validate
    :return: Tuple of (valid_worksheets, missing_worksheets)
    """
    available_worksheets = get_available_worksheets(sheet_name)
    
    valid_worksheets = []
    missing_worksheets = []
    
    for worksheet in target_worksheets:
        if worksheet in available_worksheets:
            valid_worksheets.append(worksheet)
        else:
            missing_worksheets.append(worksheet)
    
    return valid_worksheets, missing_worksheets 