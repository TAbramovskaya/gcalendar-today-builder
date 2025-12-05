from collections import namedtuple
import settings

SOURCE_OAUTH_JSON = "secret/credentials_source.json"
SOURCE_TOKEN_FILE = "secret/token_source.json"

TARGET_OAUTH_JSON = "secret/credentials_target.json"
TARGET_TOKEN_FILE = "secret/token_target.json"

SOURCE_SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
TARGET_SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


Config = namedtuple("Config", [
    "source_oauth_json",
    "target_oauth_json",
    "source_token",
    "target_token",
    "source_calendar_id",
    "target_calendar_id",
    "source_scopes",
    "target_scopes",
    "hours_ahead",
    "delete_past_days",
    "notification_minutes"
])

CFG = Config(
    source_oauth_json=SOURCE_OAUTH_JSON,
    target_oauth_json=TARGET_OAUTH_JSON,
    source_token=SOURCE_TOKEN_FILE,
    target_token=TARGET_TOKEN_FILE,
    source_scopes=SOURCE_SCOPES,
    target_scopes=TARGET_SCOPES,
    source_calendar_id=settings.SOURCE_CALENDAR_ID,
    target_calendar_id=settings.TARGET_CALENDAR_ID,
    hours_ahead=settings.HOURS_AHEAD,
    delete_past_days=settings.DELETE_PAST_DAYS,
    notification_minutes=settings.NOTIFICATION_MINUTES
)
