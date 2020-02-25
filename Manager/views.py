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

from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from User.models import Userprofile
from django.http import Http404
from User.forms import CustomUserForm, UserprofileForm, Manageruserform, ManagerprofileForm
from django.utils.datastructures import MultiValueDictKeyError


@staff_member_required
def users(request):
	return render(request, 'users.html', {'userprofiles': Userprofile.objects.all()})


@staff_member_required
def user(request, username):
	try:
		userprofile = Userprofile.objects.get(user=User.objects.get(username=username))
	except:
		raise Http404("Poll does not exist")
	
	return render(request, 'user.html', {'currentUser': userprofile})


@staff_member_required
def updateUser(request, username):
	try:
		userprofile = Userprofile.objects.get(user=User.objects.get(username=username))
	except:
		raise Http404("Poll does not exist")
	
	if request.method == 'POST':
		extended_user_form = CustomUserForm(request.POST)
		manager_userform = Manageruserform(request.POST)
		userprofile_form = UserprofileForm(request.POST)
		manager_userprofileform = ManagerprofileForm(request.POST)

		if extended_user_form.is_valid() and manager_userform.is_valid() and userprofile_form.is_valid() and manager_userprofileform.is_valid():
			userprofile.user.first_name = extended_user_form.cleaned_data.get("first_name")
			userprofile.user.last_name = extended_user_form.cleaned_data.get("last_name")
			userprofile.user.email = extended_user_form.cleaned_data.get("email")
			userprofile.user.is_staff = manager_userform.cleaned_data.get("is_staff")
			userprofile.user.save()

			userprofile.ltu_id = userprofile_form.cleaned_data.get("ltu_id")
			userprofile.favorite_food = userprofile_form.cleaned_data.get("favorite_food")
			userprofile.trubadur_member = manager_userprofileform.cleaned_data.get("trubadur_member")
			userprofile.extended_membership_status = manager_userprofileform.cleaned_data.get("extended_membership_status")
			userprofile.save()
			
			try:
				if request.POST['dateButton'] == '+12':
					userprofile.expiry_date += timedelta(days=365)
				elif request.POST['dateButton'] == '+6':
					userprofile.expiry_date += timedelta(days=186)
				elif request.POST['dateButton'] == '-12':
					userprofile.expiry_date -= timedelta(days=365)
				elif request.POST['dateButton'] == '-6':
					userprofile.expiry_date -= timedelta(days=186)
				
				userprofile.save()

			except MultiValueDictKeyError:
				userprofile.expiry_date = request.POST['date']
				userprofile.save()
				return redirect('manageUser', username)

	else:
		extended_user_form = CustomUserForm(instance=userprofile.user)
		manager_userform = Manageruserform(instance=userprofile.user)
		userprofile_form = UserprofileForm(instance=userprofile)
		manager_userprofileform = ManagerprofileForm(instance=userprofile)

	return render(request, 'updateUser.html', {'currentUser': userprofile, 'extended_user_form': extended_user_form, 'manager_userform': manager_userform, 'userprofile_form': userprofile_form, 'manager_userprofileform': manager_userprofileform})

