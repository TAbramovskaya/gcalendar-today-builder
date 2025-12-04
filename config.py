from collections import namedtuple
import args

Config = namedtuple("Config", [
    "source_oauth_json",
    "source_token",
    "target_oauth_json",
    "target_token",
    "source_calendar_id",
    "target_calendar_id",
    "hours_ahead",
    "source_scopes",
    "target_scopes"
])

CFG = Config(
    source_oauth_json=args.SOURCE_OAUTH_JSON,
    source_token=args.SOURCE_TOKEN_FILE,
    target_oauth_json=args.TARGET_OAUTH_JSON,
    target_token=args.TARGET_TOKEN_FILE,
    source_calendar_id=args.SOURCE_CALENDAR_ID,
    target_calendar_id=args.TARGET_CALENDAR_ID,
    hours_ahead=args.HOURS_AHEAD,
    source_scopes=args.SOURCE_SCOPES,
    target_scopes=args.TARGET_SCOPES
)
