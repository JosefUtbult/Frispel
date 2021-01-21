#####################################################
#													#
#	Author: Josef Utbult							#
#	Date: 13 Oct 2020								#
#													#
#	This software is written for 					#
#	Musikföreningen Frispel and is not				#
#	meant to be used for applications other 		#
#	than studying it.								#
#													#
#####################################################

from __future__ import print_function

import base64
import pickle
import os.path
from email import errors
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import date

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Mail to the person responsible for adding access
TO_MAIL = 'nicklas.lindgren@ltu.se'

# Webmasters mail
FROM_MAIL = 'frispel.webmaster@gmail.com'

# Standard mail body to send to the access person
MESSAGE_BODY = "Hej. Följande {person} behöver access till replokalen Frispel (Kultens lokal) " \
               "fr.o.m. idag t.o.m. {date}:\n" \
               "\n" \
               "{names}\n" \
               "\n" \
               "Detta är ett autogenererat mail, så om någonting är fel får du gärna " \
               "svara på det för att jag ska se det.\n" \
               "Tack på förhand.\n" \
               "\n" \
               "Josef Utbult, Webbmaster/Kassör Frispel"


def generate_service():
    # Uses a bunch of stuff. Don't really know
    try:
        with open('GoogleMail/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    except:
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    return build('gmail', 'v1', credentials=creds)


def create_message(sender, to, cc, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['cc'] = ', '.join(cc)
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }


def send_message(service, message, user_id='me'):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        return message
    except Exception as e:
        print('An error occurred when trying to send email: %s' % e)
        return None


def parse_userprofile(userprofile):
    return userprofile.ltu_id != '' and \
           len(userprofile.ltu_id.strip()) == 8 and \
           userprofile.expiry_date >= date.today()


def send_access_mail(userprofiles):
    userprofiles = userprofiles[:] if type(userprofiles) is list else [userprofiles]
    userprofiles = list(filter(parse_userprofile, userprofiles))
    if len(userprofiles) == 0:
        print(f"Unable to send access email: No correct userprofile")
        return

    names = '\n'.join([f"\t{userprofile.user.first_name} {userprofile.user.last_name} ({userprofile.ltu_id})"
                       for userprofile in userprofiles])

    month = ['Januari',
             'Februari',
             'Mars', 'April',
             'Maj', 'Juni', 'Juli',
             'Augusti',
             'September',
             'Oktober',
             'November',
             'December'][userprofiles[0].expiry_date.month - 1]
    date = f'{userprofiles[0].expiry_date.day} {month} {userprofiles[0].expiry_date.year}'

    body = MESSAGE_BODY.format(person='person', date=date, names=names)
    message = create_message(sender=FROM_MAIL,
                             to=TO_MAIL,
                             cc=[userprofile.user.email for userprofile in userprofiles],
                             subject='Access Frispel',
                             message_text=body)
    send_message(service=generate_service(), message=message)


def generate_token():
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

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
