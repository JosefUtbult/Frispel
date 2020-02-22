#####################################################
#													#
#	Author: Josef Utbult							#
#	Date: 9 Feb 2020								#
#													#
#	This software is written for 					# 
#	Musikföreningen Frispel and is not				#
#	meant to be used for applications other 		#
#	than studying it.								#
#													#
#####################################################

from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from .google_handler import pull_database

# The time slots for weekdays and correspondent weekends
WEEKDAY = [('19:00', '21:00'), ('21:00', '23:00'), ('23:00', '01:00')]
WEEKEND = [('09:00', '12:00'), ('12:00', '15:00'), ('15:00', '18:00'), ('18:00', '21:00'), ('21:00', '00:00')]
# This defines how many days ahead frispelmembers should be able to book times
DATESAHEAD = 7

# Generates dates populated with blocks within a timespan dictated by DATESAHEAD
def generate_dates():
	# Pulls all events from google within the defined timespan
	start = datetime.now().replace(hour=0, minute=0)
	end = start + timedelta(days=DATESAHEAD + 1)
	events = pull_database(start=start, end=end)

	# Generates a list of days populated with blocks
	day_list = []
	# Generates a list of all users and a list to append the users bookings
	bookings = {user.username: [] for user in User.objects.all()}
	for day in range(DATESAHEAD):
		day_list.append({
			"date": start + timedelta(days=day),
			"block": [],
			})
		# Checks blocks according to the defined time slots
		for block in (WEEKDAY if day_list[-1]['date'].weekday() < 5 else WEEKEND):
			block_start = day_list[-1]['date'].replace(hour=datetime.strptime(block[0], '%H:%M').hour, minute=datetime.strptime(block[0], '%H:%M').minute)
			block_end = day_list[-1]['date'].replace(hour=datetime.strptime(block[1], '%H:%M').hour, minute=datetime.strptime(block[1], '%H:%M').minute)
			# Fixes a special case when a time slot stretches over midnight
			while block_start > block_end:
				block_end += timedelta(days=1)

			# Checks for collisions in the events pulled from google
			collision_result = collision_detection(events, block_start, block_end)

			# If collision_result is false, that means that there where no event that
			# didn't belong to frispel occupying the time slot for the block
			if collision_result != False:
				# Appends the block. If the collision_result only is true that means
				# that no frispel user has booked that block. Otherwise, the user
				# is stored in the user key
				day_list[-1]['block'].append({
					'start': block_start,
					'end':block_end,
					'user': None if collision_result == True else collision_result['username'],
					'googleId': None if collision_result == True else collision_result['id']
				})

				if collision_result != True:
					try:
						bookings[day_list[-1]['block'][-1]['user']].append(day_list[-1]['block'][-1])
					except:
						pass

	# Returns the resulting days with there corresponding blocks and the bookings
	return day_list, bookings

# Checks if a start and end time collides with another event, and if so if this event
# is a frispel booking
def collision_detection(events, block_start, block_end):
	# Pads the start and end times to fix an off by one error
	block_start += timedelta(minutes=1)
	block_end -= timedelta(minutes=1)

	for event in events:
		# Checks time collision
		if 	block_start >= block_end or \
			block_start >= event['start'] and block_start <= event['end'] or \
			block_end >= event['start'] and block_end <= event['end'] or \
			block_start <= event['start'] and block_end >= event['end']:
			# If an event collides, checks whether this is a booking from frispel.
			# In that case, returns the whole event with username and all
			if event['frispel_booking']:
				return event
			# If the event isn't a frispel booking, returns false
			return False
	# If there is no event overlapping with the start and end time, returns true
	return True