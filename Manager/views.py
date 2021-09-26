#####################################################
#													#
#	Author: Josef Utbult							#
#	Date: 9 Feb 2020								#
#													#
#	This software is written for					# 
#	Musikföreningen Frispel and is not				#
#	meant to be used for applications other			#
#	than studying it.								#
#													#
#####################################################

from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.conf import settings
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from User.models import Userprofile
from User.forms import CustomUserForm, UserprofileForm, Manageruserform, ManagerprofileForm
from GoogleMail.google_mail import send_access_mail

# Mail to the person responsible for adding access
TO_MAIL = 'nicklas.lindgren@ltu.se'
DEBUG_TO_MAIL = 'josef@utbult.design'

# Webmasters mail
FROM_MAIL = 'frispel.webmaster@gmail.com'

# Standard mail body to send to the access person
MESSAGE_BODY = "Hej. Följande {person} behöver access till replokalen Frispel (Kultens lokal) " \
			   "fr.o.m. idag t.o.m. dennes specifierade datum.\n" \
			   "{body}" \
			   "\n" \
			   "Detta är ett autogenererat mail, så om någonting är fel får du gärna " \
			   "svara på det för att jag ska se det.\n" \
			   "Tack på förhand.\n" \
			   "\n" \
			   "Josef Utbult, Webbmaster/Kassör Frispel"



@staff_member_required
def manager(request):
	return render(request, 'manager.html')


@staff_member_required
def maillist(request):
	return render(request, 'mailList.html',
				  {'adresses': sorted(dict.fromkeys([user.email.lower() for user in User.objects.all()]))})


@staff_member_required
def trubadur(request):
	userprofiles = Userprofile.objects.filter(trubadur_member=True)
	if request.method == 'POST':
		print(request.POST)
		if 'append' in request.POST or 'date' in request.POST:
			if 'append' in request.POST and request.POST['append'] in ['6m', '12m']:
				date_obj = date.today() + timedelta(days=186 if request.POST['append'] == '6m' else 365)
			
			else:
				date_obj = date.fromisoformat(request.POST['date'])
			
			for userprofile in userprofiles:
				userprofile.application_expiry_date = date_obj
				userprofile.save()
		else:
			for userprofile in userprofiles:
				if userprofile.user.username not in request.POST:
					userprofile.trubadur_member = False
					userprofile.save()


	userprofiles = Userprofile.objects.filter(trubadur_member=True)
	return render(request, 'trubadur.html', {'userprofiles': userprofiles})


@staff_member_required
def users(request):
	userprofiles = Userprofile.objects.all()
	for userprofile in userprofiles:
		userprofile.active = userprofile.registered_expiry_date > date.today()

	return render(request, 'users.html', {'userprofiles': userprofiles})


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
		if 'append' in request.POST and request.POST['append'] in ['6m', '12m']:
			userprofile.application_expiry_date = date.today() + timedelta(days=186 if request.POST['append'] == '6m' else 365)
			userprofile.save()
		else:	 
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
				userprofile.bookings_allowed = manager_userprofileform.cleaned_data.get("bookings_allowed")
				userprofile.trubadur_member = manager_userprofileform.cleaned_data.get("trubadur_member")
				userprofile.extended_membership_status = manager_userprofileform.cleaned_data.get(
					"extended_membership_status")
				userprofile.save()

		return redirect('manageUser', username)
	
	else:
		extended_user_form = CustomUserForm(instance=userprofile.user)
		manager_userform = Manageruserform(instance=userprofile.user)
		userprofile_form = UserprofileForm(instance=userprofile)
		manager_userprofileform = ManagerprofileForm(instance=userprofile)

	return render(request, 'updateUser.html', {'currentUser': userprofile, 'extended_user_form': extended_user_form,
											   'manager_userform': manager_userform,
											   'userprofile_form': userprofile_form,
											   'manager_userprofileform': manager_userprofileform})


@staff_member_required
def register_access(request):
	changed_userprofiles = list(filter(lambda instance: instance.application_expiry_date != instance.registered_expiry_date, Userprofile.objects.all()))

	if request.method == 'POST':
		print(request.POST)
		if 'reset' in request.POST:
			userprofile = Userprofile.objects.get(user=User.objects.get(username=request.POST['reset']))
			userprofile.application_expiry_date = userprofile.registered_expiry_date
			userprofile.save()
		else:
			mail = generate_mail(changed_userprofiles)
			send_access_mail(mail)
			
			for userprofile in changed_userprofiles:
				userprofile.registered_expiry_date = userprofile.application_expiry_date
				userprofile.save()

		changed_userprofiles = list(filter(lambda instance: instance.application_expiry_date != instance.registered_expiry_date, Userprofile.objects.all()))
	return render(request, 'registerAccess.html', {'currentUser': 'userprofile', 'changed_userprofiles': changed_userprofiles, 'mail': generate_mail(changed_userprofiles)})


def generate_mail(userprofiles):
	month = [
		'Januari',
		'Februari',
		'Mars', 
		'April',
		'Maj', 
		'Juni', 
		'Juli',
		'Augusti',
		'September',
		'Oktober',
		'November',
		'December'
	] 

	date_set = {}
	for instance in userprofiles:
		if instance.application_expiry_date not in date_set:
			date_set[instance.application_expiry_date] = []
		date_set[instance.application_expiry_date].append(instance)
	
	body = ""
	for instance in date_set:
		body += f"\nFöljande {'personer' if len(date_set[instance]) > 1 else 'person'} behöver acces t.o.m {instance.day} {month[instance.month - 1]} {instance.year}:\n"
		for userprofile in date_set[instance]:
			body += f"\t{userprofile.user.first_name} {userprofile.user.last_name} ({userprofile.ltu_id.lower()})\n"

	cc = [instance.user.email for instance in userprofiles] if not settings.DEBUG else []
	cc += [FROM_MAIL]
	
	return {
				'from': FROM_MAIL,
				'to': TO_MAIL if not settings.DEBUG else DEBUG_TO_MAIL, 
				'cc': cc, 
				'title': 'Access to frispel', 
				'body': MESSAGE_BODY.format(person='person', body=body)
			}
