import datetime as dt
from dateutil import tz
from logger import get_logger

log = get_logger(__name__)


def build_target_event(ev, notification_minutes: tuple[int, ...]):
    summary = ev.get("summary", "")
    start = ev["start"]
    end = ev["end"]

    reminders = {
        "useDefault": False,
        "overrides": [
            {"method": "popup", "minutes": m} for m in notification_minutes
        ],
    }

    return {
        "summary": summary,
        "start": start,
        "end": end,
        "reminders": reminders,
    }


def insert_event(service, calendar_id: str, event_body: dict):
    return service.events().insert(
        calendarId=calendar_id,
        body=event_body,
        sendUpdates="none",
    ).execute()


def write_events(service, calendar_id: str, events: list[dict], notification_minutes: tuple[int, ...]):
    log.info("Inserting events...")
    for ev in events:
        target_event = build_target_event(ev, notification_minutes)
        insert_event(service, calendar_id, target_event)
    log.info("Finished inserting events.")


def clear_target(service, calendar_id: str, delete_past_days: int, hours: int):
    tzinfo = tz.gettz("UTC")
    today = dt.datetime.now(tzinfo).date()
    today_midnight = dt.datetime.combine(today, dt.time.min, tzinfo)

    # Clean from M days ago and until N hours after midnight
    start = today_midnight - dt.timedelta(days=delete_past_days)
    end = today_midnight + dt.timedelta(hours=hours)

    time_min = start.isoformat()
    time_max = end.isoformat()

    events = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        showDeleted=False,
    ).execute().get("items", [])

    log.info(f"Deleting {len(events)} events from target...")

    for ev in events:
        try:
            service.events().delete(
                calendarId=calendar_id,
                eventId=ev["id"],
                sendUpdates="none"
            ).execute()
        except Exception as e:
            log.error(f"Failed to delete {ev['id']}: {e}")

    log.info("Done with clean-up.")
