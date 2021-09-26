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

from django.contrib.auth import authenticate
from django.contrib.auth import login as super_login
from django.contrib.auth import logout as super_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import Content.views as content_views
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserForm, UserprofileForm
from .models import Userprofile

# Gives the login page, parses the form and redirects on successful login
def login(request):

	if request.method == 'POST':
		form = {'username': request.POST.get('username'), 'password': request.POST.get('password')}
		user = authenticate(request, username=form.get('username'), password=form.get('password'))
		if user is not None:
			super_login(request, user)
			try:
				return redirect(request.get_full_path().split('?next=')[1])
			except IndexError:
				return redirect('home')

	else:
		form = {'username': '', 'password': ''}

	return render(request, 'login.html', {'form': form, 'result': '' if not request.method == 'POST' else 'Incorrect username or password'})

# Runs the logout function and gives the logout page
def logout(request):
	super_logout(request)
	return render(request, 'logout.html')

# Gives the sign up page and generates a user on successful 
def signup(request):

	if request.method == 'POST':
		# Generates the standard user creation form, an extended user form and a 
		# form for the userprofile
		user_form = UserCreationForm(request.POST)
		extended_user_form = CustomUserForm(request.POST)
		userprofile_form = UserprofileForm(request.POST)

		# Validates all the forms
		if user_form.is_valid() and extended_user_form.is_valid() and userprofile_form.is_valid():
			# Stores the user form and manually inserts the data from the extended user form 
			# into the newly created user
			user = user_form.save(commit=False)
			user.first_name = extended_user_form.cleaned_data.get("first_name")
			user.last_name = extended_user_form.cleaned_data.get("last_name")
			user.email = extended_user_form.cleaned_data.get("email")
			user.save()

			# Manually sets the membership status of the newly created userprofile and
			# stores it
			userprofile = userprofile_form.save(commit=False)
			userprofile.user = user
			userprofile.save()

			# Authenticates and signs in the new user
			username = user_form.cleaned_data.get('username')
			raw_password = user_form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			super_login(request, user)
			return redirect('notAMember')

	else:
		# Creates empty forms for the get method
		user_form = UserCreationForm()
		extended_user_form = CustomUserForm()
		userprofile_form = UserprofileForm()
	
	return render(request, 'signup.html', {'user_form': user_form, 'extended_user_form': extended_user_form, 'userprofile_form': userprofile_form})


# The users account page
@login_required(login_url='login')
def account(request):
	return render(request, 'account.html', {'userprofile': Userprofile.objects.get(user=request.user)})

# The page for a user to update its userdata
@login_required(login_url='login')
def updateAccount(request):

	if request.method == 'POST':
		# Uses the extended user form and the userprofile form
		extended_user_form = CustomUserForm(request.POST, instance=request.user)
		userprofile_form = UserprofileForm(request.POST, instance=Userprofile.objects.get(user=request.user))

		if extended_user_form.is_valid() and userprofile_form.is_valid():
			extended_user_form.save()
			userprofile_form.save()

			return redirect('account')

	else:
		extended_user_form = CustomUserForm(instance=request.user)
		userprofile_form = UserprofileForm(instance=Userprofile.objects.get(user=request.user))

	return render(request, 'updateAccount.html', {'extended_user_form': extended_user_form, 'userprofile_form': userprofile_form})

