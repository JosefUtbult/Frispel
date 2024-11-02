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

from Frispel.settings import SECRETS_DIR

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

TOKEN_FILE = os.path.join(SECRETS_DIR, 'google_mail_token.pickle')

def generate_service():
    # Uses a bunch of stuff. Don't really know
    with open(TOKEN_FILE, 'rb') as token:
        creds = pickle.load(token)

    service = build('gmail', 'v1', credentials=creds)
    
    if not creds.valid:
        print("Credentials are invalid for this token. It needs to be re generated")

    return service



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


def send_access_mail(mail):

    message = create_message(sender=mail['from'],
        to=mail['to'],
        cc=mail['cc'],
        subject=mail['title'],
        message_text=mail['body'])
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


if __name__ == "__main__":
    class moc_profile:
        ltu_id = 'testes-4'
        expiry_date = date.today()

        class user:
            first_name = 'Test'
            last_name = 'Test'
            email = 'josef.utbult@hotmail.com'


    send_access_mail(moc_profile, debug=True)
