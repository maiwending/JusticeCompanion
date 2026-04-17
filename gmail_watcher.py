import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import time
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Handles Gmail API integration and watching for new emails
class GmailWatcher:
    def __init__(self, user_id='me'):
        self.creds = None
        self.user_id = user_id
        self.service = self.authenticate()

    def authenticate(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=8080)  # Use fixed port for redirect URI
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        return build('gmail', 'v1', credentials=self.creds)

    def watch_for_email(self, sender_email, callback, poll_interval=30):
        print(f"Watching for emails from {sender_email}...")
        seen_ids = set()
        while True:
            try:
                results = self.service.users().messages().list(userId=self.user_id, q=f'from:{sender_email}').execute()
                messages = results.get('messages', [])
                for msg in messages:
                    msg_id = msg['id']
                    if msg_id not in seen_ids:
                        seen_ids.add(msg_id)
                        message = self.service.users().messages().get(userId=self.user_id, id=msg_id, format='full').execute()
                        callback(message)
            except HttpError as error:
                print(f'An error occurred: {error}')
            time.sleep(poll_interval)
