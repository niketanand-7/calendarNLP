from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Feature 1: List all calendars
    print("Fetching all calendars:")
    calendar_list = service.calendarList().list().execute().get('items', [])
    for calendar in calendar_list:
        print(calendar['summary'])

    # Feature 2: Create a new calendar
    new_calendar = {
        'summary': 'School Calendar',
        'timeZone': 'America/New_York'
    }
    created_calendar = service.calendars().insert(body=new_calendar).execute()
    print(f"Created calendar: {created_calendar['id']}")

    # Feature 3: Insert an event
    event = {
        'summary': 'Python Meeting',
        'description': 'A meeting to discuss Python projects.',
        'start': {
            'dateTime': (datetime.utcnow() + timedelta(days=1)).isoformat(),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': (datetime.utcnow() + timedelta(days=1, hours=1)).isoformat(),
            'timeZone': 'America/New_York',
        },
    }
    created_event = service.events().insert(calendarId=created_calendar['id'], body=event).execute()
    print(f"Created event: {created_event['id']}")


if __name__ == '__main__':
    main()