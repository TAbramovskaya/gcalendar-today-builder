### Google Calendar Today Builder

This project synchronizes a subset of upcoming Google Calendar events from a source calendar to a target calendar.

### What the script does

- Fetches events from the source Google Calendar for a defined window (e.g., N hours from today’s midnight).

- Ignores all-day and cancelled events.

- Cleans the target calendar for the specified period (including optional days before today).

- Inserts new events into the target calendar with (and only) original start/end time and summary, and custom reminder settings.

- Uses separate OAuth credentials for source and target Google accounts.

### Required Google API Credentials

This application uses the Google Calendar API and therefore requires OAuth 2.0 Client ID credentials created in Google Cloud Console.

Two sets of credentials are required. 

- Source credentials authorize the script to read from the source calendar. They must be granted read-only scopes.

- Target credentials authorize the script to write events to the target calendar. They must be granted write scopes.

Both credential sets can come from the same Google Cloud project. The credentials are created in the Google Cloud Console, inside a project where the Google Calendar API is enabled. For background on creating these credentials, see the [Google Calendar API Python Quickstart](https://developers.google.com/workspace/calendar/api/quickstart/python#set-up-environment).

All credentials and OAuth tokens must be stored in `secret/` directory.

### Configuration

All runtime configuration (calendar IDs, time windows, reminders) is stored in `settings.py`.
