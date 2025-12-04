#!/usr/bin/env python3
from __future__ import annotations

from config import CFG
from auth import load_credentials, build_service
from fetcher import fetch_upcoming_events
from writer import build_target_event, insert_event, clear_target
from logger import get_logger

log = get_logger(__name__)


def main():
    src_creds = load_credentials(CFG.source_oauth_json, CFG.source_token, CFG.source_scopes, "SOURCE")
    tgt_creds = load_credentials(CFG.target_oauth_json, CFG.target_token, CFG.target_scopes, "TARGET")

    src_service = build_service(src_creds)
    tgt_service = build_service(tgt_creds)

    events = fetch_upcoming_events(src_service, CFG.source_calendar_id, CFG.hours_ahead)

    clear_target(tgt_service, CFG.target_calendar_id, CFG.hours_ahead)

    log.info("Inserting events...")
    for ev in events:
        target_event = build_target_event(ev)
        insert_event(tgt_service, CFG.target_calendar_id, target_event)
    log.info("Finished.")


if __name__ == "__main__":
    main()
