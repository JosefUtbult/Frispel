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
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from User.models import Userprofile

@staff_member_required
def users(request, username=None):
	if username == None:
		return render(request, 'users.html', {'userprofiles': Userprofile.objects.all()})

	return render(request, 'user.html', {'currentUser': username})