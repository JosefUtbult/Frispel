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
from django.shortcuts import render
from django.shortcuts import redirect as django_redirect
import Content.views as content_views
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserForm, UserprofileForm
from django.contrib.auth.models import User
from .models import Userprofile
from django.contrib import messages

# Is called by the CAS. If this user already has logged in and created a user profile, redirect to home
def redirect(request, lang=None):
    print(f'Got request: {request} for user: ${request.user}')

    userprofile, created = Userprofile.objects.get_or_create(user=request.user)
    
    if created or not userprofile.is_set_up:
        if lang:
            return django_redirect('signup', lang=lang)
        else:
            return django_redirect('signup')

    if lang:
        return django_redirect('home', lang=lang)
    else:
        return django_redirect('home')


def check_set_up(request, lang):
    try:
        user = User.objects.get(username=request.user)
        userprofile = Userprofile.objects.get(user=user)

        if not userprofile.is_set_up:
            raise Exception
    except:
        if lang and lang == 'en':
            messages.add_message(request, messages.INFO, 'You have to fill in further information about yourself')
        else:
            messages.add_message(request, messages.INFO, 'Du måste fylla i mer information om dig själv')

        if lang:
            return django_redirect('redirect', lang)
        else:
            return django_redirect('redirect')

    return True

# Gives the sign up page and generates a user on successful 
@login_required(login_url='login')
def signup(request, lang=None):

    if request.method == 'POST':
        # Generates a custom user form and a 
        # form for the userprofile
        extended_user_form = CustomUserForm(request.POST)
        userprofile_form = UserprofileForm(request.POST)

        # Validates all the forms
        if extended_user_form.is_valid() and userprofile_form.is_valid():
            # Stores the user form and manually inserts the data from the extended user form 
            # into the newly created user
            request.user.first_name = extended_user_form.cleaned_data.get("first_name")
            request.user.last_name = extended_user_form.cleaned_data.get("last_name")
            request.user.email = extended_user_form.cleaned_data.get("email")
            request.user.save()

            # Manually sets the membership status of the newly created userprofile and
            # stores it
            userprofile = userprofile_form.save(commit=False)
            userprofile.user = request.user
            userprofile.is_set_up = True
            userprofile.save()

            if lang:
                return django_redirect('home', lang)
            else:
                return django_redirect('home')
    else:
        # Creates empty forms for the get method
        extended_user_form = CustomUserForm()
        userprofile_form = UserprofileForm()
    
    return render(request, 'signup.html', {'extended_user_form': extended_user_form, 'userprofile_form': userprofile_form, 'lang': lang})


# The users account page
@login_required(login_url='login')
def account(request, lang=None):
    is_setup = check_set_up(request, lang)
    return is_setup if is_setup != True else render(request, 'account.html', {'userprofile': Userprofile.objects.get(user=request.user)})

# The page for a user to update its userdata
@login_required(login_url='login')
def updateAccount(request, lang=None):
    is_setup = check_set_up(request, lang)
    if is_setup != True:
        return is_setup

    if request.method == 'POST':
        # Uses the extended user form and the userprofile form
        extended_user_form = CustomUserForm(request.POST, instance=request.user)
        userprofile_form = UserprofileForm(request.POST, instance=Userprofile.objects.get(user=request.user))

        if extended_user_form.is_valid() and userprofile_form.is_valid():
            extended_user_form.save()
            userprofile_form.save()

            return django_redirect('account')

    else:
        extended_user_form = CustomUserForm(instance=request.user)
        userprofile_form = UserprofileForm(instance=Userprofile.objects.get(user=request.user))

    return render(request, 'updateAccount.html', {'extended_user_form': extended_user_form, 'userprofile_form': userprofile_form})

