#####################################################
#                                                   #
# Author: Josef Utbult                              #
# Date: 9 Feb 2020                                  #
#                                                   #
# This software is written for                      # 
# Musikföreningen Frispel and is not                #
# meant to be used for applications other           #
# than studying it.                                 #
#                                                   #
#####################################################

from __future__ import print_function
from datetime import datetime, date, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pyrfc3339 import parse as RFC3339_parse

# URL for googles scope
# If modifying these scopes, delete the file token.pickle and run the generate_token function
SCOPES = ['https://www.googleapis.com/auth/calendar']
# The title that will be inserted into the calendar for a booking, and searched for
# on pulling
EVENTTITLE = 'Booked by Frispel'
# The id of the google calendar
CALENDARID = '4u2k2reraaaa3cb1ekho0kdjic@group.calendar.google.com'
# The amount of events that should be pulled from google every time
MAXRESULTSPERREQUEST = 100


# Sets up a google service
def generate_service():
    # Uses a bunch of stuff. Don't really know
    try:
        with open('GoogleCalendar/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    except:
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    return build('calendar', 'v3', credentials=creds)


# Requesting events around a start time
def pull_events(start):
    service = generate_service()
    start = start.isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=CALENDARID, timeMin=start,
                                          maxResults=MAXRESULTSPERREQUEST, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])


# Pulls the calendar from google and converts the data to a more managable set
def pull_database(start, end):
    last_booked_start_instance = start
    events = []

    # Pulls and appends events untill the last event is starting after the end time
    while last_booked_start_instance <= end:
        events += pull_events(last_booked_start_instance)
        last_booked_start_instance, last_booked_end_instance = googleresult_to_dateTime(events[-1])

    # Formats the events
    results = []
    for instance in events:
        # Converts to a block from an google event
        result = generate_block(instance)
        # Checks if the event starts after the end time, as google sends the events
        # in chunks sized by MAXRESULTSPERREQUEST
        if result['start'] > end:
            return results

        results.append(result)
    # Returns the parsed and converted events
    return results


# Parses the resulting event from google to a smaller and easier to understand block
def generate_block(googleresult):
    # Gets the start and end of the block
    start, end = googleresult_to_dateTime(googleresult)

    id = googleresult['id']
    # Tries to check if the title of the event corresponds with EVENTTITLE and if
    # so, tries to set the username of the booking to the description of the event
    try:
        frispel_booking = (googleresult['summary'] == EVENTTITLE)
    except KeyError:
        frispel_booking = False

    if frispel_booking:
        try:
            username = googleresult['description']
        except KeyError:
            username = None
            frispel_booking = False
    else:
        username = None
    # Returns the resulting block
    return {
        'id': id,
        'start': start,
        'end': end,
        'frispel_booking': frispel_booking,
        'username': username
    }


# Converts the timecode from google to a dateTime object
def googleresult_to_dateTime(googleresult):
    # Tries to retrieve the dateTime from googles result. This fails when the event
    # is an whole date event. In this case it will pull the start time and substitute
    # the end time with 23 hours and 58 offset from the start time
    try:
        # Uses the pyrfc3339 library to parse from RFC3339 standard to a datetime object
        return (RFC3339_parse(googleresult['start']['dateTime']).replace(tzinfo=None),
                RFC3339_parse(googleresult['end']['dateTime']).replace(tzinfo=None))
    except KeyError as e:
        return (datetime.strptime(googleresult['start']['date'], "%Y-%m-%d"),
                datetime.strptime(googleresult['end']['date'], "%Y-%m-%d").replace(hour=23, minute=58) - timedelta(
                    days=1))


# Adds an event to the google calendar to book the time slot
def book_block(user, start, end):
    service = generate_service()
    # Generates an event with the start and endtime, the EVENTTITLE as title and
    # the username as description
    new_event = service.events().insert(calendarId=CALENDARID,
                                        body={
                                            "summary": EVENTTITLE,
                                            "description": user,
                                            "start": {"dateTime": start.isoformat(), "timeZone": 'Europe/Stockholm'},
                                            "end": {"dateTime": end.isoformat(), "timeZone": 'Europe/Stockholm'},
                                        }
                                        ).execute()


# Tries to delete an event from the google calendar
def unbook_block(user, start, end, id):
    service = generate_service()

    # Tries to retrieve the event by its id. Returns false if the event doesn't exist
    try:
        event = service.events().get(calendarId=CALENDARID, eventId=id).execute()
    except HttpError:
        return False

    # Converts the time, checks so the event time checks out and that the users username
    # is prescient in the description
    event_start, event_end = googleresult_to_dateTime(event)
    if start != event_start or end != event_end or user.username != event['description']:
        return False
    # Deletes the event
    service.events().delete(calendarId=CALENDARID, eventId=id).execute()
    return True


# This is googles own code. It generates a token if that is somehow not working
def generate_token():
    """Shows basic usage of the People API.
	Prints the name of the first 10 connections.
	"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    # Call the People API
    print('List 10 connection names')
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=10,
        personFields='names,emailAddresses').execute()
    connections = results.get('connections', [])

    for person in connections:
        names = person.get('names', [])
        if names:
            name = names[0].get('displayName')
            print(name)
