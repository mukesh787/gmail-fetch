from fastapi import FastAPI
from typing import List
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import base64
import json
import re
from email import message_from_bytes

# Scopes required to read Gmail messages
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

app = FastAPI()

# Authenticate and create Gmail API service
def get_gmail_service():
    creds = None
    token_file = 'token.json'

    # Load existing token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If no valid token, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for future use
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_sender_and_subject(message_payload):
    headers = message_payload.get('headers', [])
    sender = subject = ''
    for header in headers:
        if header['name'].lower() == 'from':
            sender = header['value']
        if header['name'].lower() == 'subject':
            subject = header['value']
    return sender, subject


@app.get("/emails", response_model=List[dict])
def read_last_200_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', maxResults=200).execute()
    messages = results.get('messages', [])

    email_list = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='metadata', metadataHeaders=['From', 'Subject']).execute()
        sender, subject = get_sender_and_subject(msg_data['payload'])
        email_list.append({'sender': sender, 'subject': subject})

    return email_list
