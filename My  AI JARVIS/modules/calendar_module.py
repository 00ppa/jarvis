"""
JARVIS Google Calendar Module
Cloud synchronization for events and reminders
"""

import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import GOOGLE_CALENDAR_ID

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarManager:
    """Manage Google Calendar events and reminders."""
    
    def __init__(self):
        self.creds = self._authenticate()
        self.service = build('calendar', 'v3', credentials=self.creds) if self.creds else None

    def _authenticate(self):
        """Authenticate with Google Calendar API."""
        creds = None
        # The file token.json stores the user's access and refresh tokens.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("⚠️ credentials.json not found. Please follow the setup guide.")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def add_event(self, summary, start_time, end_time=None, description=None, location=None):
        """Add an event to the calendar."""
        if not self.service:
            return "⚠️ Calendar service not initialized."

        if not end_time:
            # Default to 1 hour event
            dt = datetime.datetime.fromisoformat(start_time)
            end_time = (dt + datetime.timedelta(hours=1)).isoformat()

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
        }

        try:
            event = self.service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=event).execute()
            return f"✅ Event created: {event.get('htmlLink')}"
        except HttpError as error:
            return f"❌ An error occurred: {error}"

    def get_upcoming_events(self, max_results=10):
        """Get upcoming events."""
        if not self.service:
            return []

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        try:
            events_result = self.service.events().list(calendarId=GOOGLE_CALENDAR_ID, timeMin=now,
                                                  maxResults=max_results, singleEvents=True,
                                                  orderBy='startTime').execute()
            return events_result.get('items', [])
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

# Singleton instance
_calendar_instance = None

def get_calendar_manager():
    """Get the singleton calendar manager instance."""
    global _calendar_instance
    if _calendar_instance is None:
        _calendar_instance = CalendarManager()
    return _calendar_instance
