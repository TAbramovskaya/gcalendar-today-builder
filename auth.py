from __future__ import annotations

import os
from typing import Optional

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def load_credentials(oauth_json: str, token_file: str, scopes: list[str], label: str) -> Credentials:
    creds: Optional[Credentials] = None

    # Load existing token if present
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)

    # If no valid credentials, perform OAuth login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(oauth_json, scopes)
            creds = flow.run_local_server(
                port=0,
                authorization_prompt_message=f"🔑 Please authorize {label} account.",
                success_message=f"✅ {label} account authorized successfully!"
            )

        # Save new token
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds


def build_service(creds: Credentials):
    return build("calendar", "v3", credentials=creds, cache_discovery=False)
