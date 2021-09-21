from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def create_draft(service, user_id, message_body):
	"""Create and insert a draft email. Print the returned draft's message and id.

	Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	message_body: The body of the email message, including headers.

	Returns:
	Draft object, including draft id and message meta data.
	"""
	try:
		message = {'message': message_body}
		draft = service.users().drafts().create(userId=user_id, body=message).execute()

		print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))

		return draft
	except errors.HttpError as error:
		print('An error occurred: %s' % error)
	
	return None


def send_message(service, user_id, message):
	"""Send an email message.

	Args:
	service: Authorized Gmail API service instance.
	user_id: User's email address. The special value "me"
	can be used to indicate the authenticated user.
	message: Message to be sent.

	Returns:
	Sent Message.
	"""
	try:
		message = (service.users().messages().send(userId=user_id, body=message).execute())
		print('Message Id: %s' % message['id'])
		return message
	except errors.HttpError as error:
		print('An error occurred: %s' % error)


def create_message(sender, to, subject, message_text):
	"""Create a message for an email.

	Args:
	sender: Email address of the sender.
	to: Email address of the receiver.
	subject: The subject of the email message.
	message_text: The text of the email message.

	Returns:
	An object containing a base64url encoded email object.
	"""
	message = MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


# This is googles own code. It generates a token if that is somehow not working
def generate_token():
	"""Shows basic usage of the Gmail API.
	Lists the user's Gmail labels.
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

	return service

SERVICE = generate_token()

message = create_message(sender='frispel.webmaster@gmail.com', to='josef.utbult@gmail.com' , subject='Hello World', message_text='This is a test')
print(send_message(service=SERVICE, user_id='me', message=message))