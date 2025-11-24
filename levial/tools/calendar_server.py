import os
import datetime
import logging
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("calendar_server")

# Define scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Initialize FastMCP
mcp = FastMCP("Google Calendar")

def get_service():
    """Authenticate and return the Calendar service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError("credentials.json not found. Please download it from Google Cloud Console.")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

@mcp.tool()
def list_upcoming_events(max_results: int = 10) -> str:
    """
    List the upcoming events on the user's primary calendar.
    """
    try:
        service = get_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=max_results, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return "No upcoming events found."
        
        result = "Upcoming events:\n"
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            result += f"- {start}: {event['summary']}\n"
        return result
    except Exception as e:
        return f"Error fetching events: {str(e)}"

@mcp.tool()
def create_event(summary: str, start_time: str, end_time: str, description: str = "") -> str:
    """
    Create a new event on the primary calendar.
    Args:
        summary: Title of the event.
        start_time: Start time in ISO format (e.g., '2023-10-27T10:00:00').
        end_time: End time in ISO format.
        description: Optional description.
    """
    try:
        service = get_service()
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC', # Assuming UTC for simplicity, should be configurable
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event.get('htmlLink')}"
    except Exception as e:
        return f"Error creating event: {str(e)}"

if __name__ == "__main__":
    mcp.run()
