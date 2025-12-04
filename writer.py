import datetime as dt
from dateutil import tz
from logger import get_logger

log = get_logger(__name__)


def attendee_count(ev):
    attendees = ev.get("attendees", [])
    statuses_to_count = {"accepted", "needsAction", None}

    count = sum(a.get("responseStatus") in statuses_to_count for a in attendees)

    organizer = ev.get("organizer", {})
    if organizer.get("self"):
        # But do not double count organizer if she/he is also in attendees
        in_attendees = any(a.get("self") for a in attendees)
        if not in_attendees:
            count += 1

    return count


def build_target_event(ev):
    summary = ev.get("summary", "")
    start = ev["start"]
    end = ev["end"]

    reminders = {
        "useDefault": False,
        "overrides": [
            {"method": "popup", "minutes": 10},
            {"method": "popup", "minutes": 2},
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


def clear_target(service, calendar_id, hours: int):
    tzinfo = tz.gettz("UTC")
    now = dt.datetime.now(tzinfo)
    end = now + dt.timedelta(hours=hours)

    time_min = now.isoformat()
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
