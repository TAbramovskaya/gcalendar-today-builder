import datetime as dt
from dateutil import tz
from logger import get_logger

log = get_logger(__name__)


def is_all_day(ev):
    return "date" in ev.get("start", {})


def is_cancelled(ev):
    return ev.get("status") == "cancelled"


def fetch_upcoming_events(service, calendar_id: str, hours: int):
    tzinfo = tz.gettz("UTC")
    now = dt.datetime.now(tzinfo)
    end = now + dt.timedelta(hours=hours)

    time_min = now.isoformat()
    time_max = end.isoformat()

    resp = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy="startTime",
        showDeleted=False,
    ).execute()

    events = resp.get("items", [])
    cleaned = []

    for ev in events:
        if is_cancelled(ev):
            continue
        if is_all_day(ev):
            continue
        cleaned.append(ev)

    log.info(f"Found {len(cleaned)} events to copy.")
    return cleaned
