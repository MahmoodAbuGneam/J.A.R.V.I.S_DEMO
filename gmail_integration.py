# gmail_integration.py

from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_recent_emails(creds, max_results=10):
    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_results).execute()
        messages = results.get('messages', [])

        if not messages:
            return "No messages found."
        
        email_list = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = {
                'id': msg['id'],
                'snippet': msg['snippet'],
                'sender': '',
                'subject': ''
            }
            
            headers = msg['payload']['headers']
            for header in headers:
                if header['name'] == 'From':
                    email_data['sender'] = header['value']
                if header['name'] == 'Subject':
                    email_data['subject'] = header['value']
            
            email_list.append(email_data)

        return email_list

    except HttpError as error:
        return f"An error occurred: {error}"

def main():
    try:
        creds = authenticate()
        emails = get_recent_emails(creds)
        
        if isinstance(emails, str):
            print(emails)  # This will print error messages or "No messages found."
        else:
            for email in emails:
                print(f"From: {email.get('sender', 'Unknown')}")
                print(f"Subject: {email.get('subject', 'No subject')}")
                print(f"Snippet: {email.get('snippet', 'No snippet available')}\n")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()