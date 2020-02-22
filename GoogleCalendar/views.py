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

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from .dateparser import *
from .google_handler import book_block, unbook_block
from User.models import Userprofile

@login_required(login_url='login')
def calendar(request):

	# Checks if you want to book or unbook a block
	if request.method == 'POST':
		if request.POST['button'] == 'Book':
			#Parsing start and end time
			start = datetime.strptime(request.POST['start'], "%H %M %d %m %Y")
			end = datetime.strptime(request.POST['end'], "%H %M %d %m %Y")
			
			# Check is someone has messed with the form and changed the time
			if collision_detection == True:
				messages.warning(request, 'You just tried to book an occupied time slot. Please don\'t try that.')
			elif start > datetime.now() + timedelta(days=DATESAHEAD):
				messages.warning(request, 'You just tried to book a time to far in the future. Please don\'t try that.')
			else:
				book_block(user=request.user.username, start=start, end=end)

		elif request.POST['button'] == 'Unbook':

			start = datetime.strptime(request.POST['start'], "%H %M %d %m %Y")
			end = datetime.strptime(request.POST['end'], "%H %M %d %m %Y")
			
			#Tries to unblock a timeslot. Gets false on unsuccessful try
			if not unbook_block(user=request.user, start=start, end=end, id=request.POST['googleId']):
				messages.warning(request, "You tried to unbook a block not booked by you. Please don\'t try that.")
	
	date_list, bookings = generate_dates()
	bookings = bookings[request.user.username]
	return render(request, 'calendar.html', {'date_list': date_list, 'bookings': bookings, 'userprofile': Userprofile.objects.get(user=request.user)})
