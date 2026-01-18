from __future__ import annotations

import os
from typing import Optional

from google.auth.exceptions import RefreshError
# noinspection PyPackageRequirements
from google.oauth2.credentials import Credentials
# noinspection PyPackageRequirements
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from logger import get_logger

log = get_logger(__name__)


def load_credentials(oauth_json: str, token_file: str, scopes: list[str], label: str) -> Credentials:
    creds: Optional[Credentials] = None

    # Load existing token if present
    if os.path.exists(token_file):
        log.info(f"[{label}] Loading existing token from {token_file}.")
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    else:
        log.info(f"[{label}] No existing token found...")

    # If no valid credentials, perform OAuth login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            log.info(f"[{label}] Token expired, attempting refresh...")
            try:
                creds.refresh(Request())
                log.info(f"[{label}] Token refreshed successfully.")
            except RefreshError as e:
                log.warning(f"[{label}] Token refresh failed: {e}")
                try:
                    os.remove(token_file)
                    log.warning(f"[{label}] Deleted invalid token file {token_file}.")
                except FileNotFoundError:
                    pass
                creds = _run_oauth_flow(oauth_json, scopes, label)
        else:
            creds = _run_oauth_flow(oauth_json, scopes, label)

        with open(token_file, "w") as token:
            token.write(creds.to_json())
            log.info(f"[{label}] Token saved to {token_file}.")

    return creds


def _run_oauth_flow(oauth_json: str, scopes: list[str], label: str) -> Credentials:
    log.info(f"[{label}] Starting browser OAuth flow...")
    flow = InstalledAppFlow.from_client_secrets_file(oauth_json, scopes)
    creds = flow.run_local_server(
                port=0,
                authorization_prompt_message=f"🔑 Please authorize {label} account.",
                success_message=f"{label} account authorized successfully!"
            )
    log.info(f"[{label}] OAuth flow completed.")
    return creds

def build_service(creds: Credentials):
    return build("calendar", "v3", credentials=creds, cache_discovery=False)
