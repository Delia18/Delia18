"""Simple script to fetch emails from Gmail using the Gmail API.

Setup instructions:
1. Go to https://console.cloud.google.com/apis/credentials and create an
   OAuth 2.0 Client ID for a Desktop application.
2. Download the generated `credentials.json` file and place it in the same
   directory as this script.
3. Install dependencies:
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
4. Run this script. A browser window will open asking you to authorize
   the application. After authorization, a `token.json` file is stored with
   your access token for subsequent runs.
"""

from __future__ import print_function

import os.path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# The scope grants read-only access to Gmail.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate() -> "build":
    """Authenticate the user and return a Gmail API service object."""
    creds: Optional[Credentials] = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service


def list_messages(service, user_id: str = "me", max_results: int = 10) -> None:
    """Print snippets of the user's most recent messages."""
    response = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
    messages = response.get("messages", [])
    for msg in messages:
        msg_data = service.users().messages().get(userId=user_id, id=msg["id"]).execute()
        snippet = msg_data.get("snippet")
        print("Message snippet:", snippet)


if __name__ == "__main__":
    gmail_service = authenticate()
    list_messages(gmail_service)
