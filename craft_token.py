from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pathlib import Path
import os
import sys
import argparse

import json
import os

# Variables
SCOPES = ['https://www.googleapis.com/auth/admin.reports.audit.readonly']
TOKEN_PATH = "token.json"

def BuildCredentials(tokenPath):

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(tokenPath):
        print(tokenPath)
        creds = Credentials.from_authorized_user_file(tokenPath, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=1234)
        # Save the credentials for the next run
        with open(tokenPath, 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'reports_v1', credentials=creds)
    return service



if __name__ == "__main__":

    # Generate token file
    print("Build token")
    service = BuildCredentials(TOKEN_PATH)
    print("Token built!")

    
