#####################################################
#                                                   #
#   Author: Josef Utbult                            #
#   Date: 9 Feb 2020                                #
#                                                   #
#   This software is written for                    # 
#   Musikföreningen Frispel and is not              #
#   meant to be used for applications other         #
#   than studying it.                               #
#                                                   #
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
from Frispel.settings import logger

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
               "Elias Falk, Ordförande Frispel"

@staff_member_required
def manager(request, lang=None):
    return render(request, 'manager.html', {'unapplied_access': get_unapplied_access(), 'lang': lang})


@staff_member_required
def maillist(request, lang=None):
    return render(request, 'mailList.html', {'adresses': sorted(dict.fromkeys([user.email.lower() for user in User.objects.all()])), 'unapplied_access': get_unapplied_access(), 'lang': lang})


@staff_member_required
def trubadur(request, lang=None):
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
    return render(request, 'trubadur.html', {'userprofiles': userprofiles, 'unapplied_access': get_unapplied_access(), 'lang': lang})


@staff_member_required
def users(request, lang=None):
    userprofiles = Userprofile.objects.all()
    for userprofile in userprofiles:
        userprofile.active = userprofile.registered_expiry_date > date.today()

    return render(request, 'users.html', {'userprofiles': userprofiles, 'unapplied_access': get_unapplied_access(), 'lang': lang})


@staff_member_required
def user(request, username, lang=None):
    try:
        userprofile = Userprofile.objects.get(user=User.objects.get(username=username))
    except:
        raise Http404("Poll does not exist")

    return render(request, 'user.html', {'currentUser': userprofile, 'unapplied_access': get_unapplied_access(), 'lang': lang})


@staff_member_required
def updateUser(request, username, lang=None):
    try:
        userprofile = Userprofile.objects.get(user=User.objects.get(username=username))
    except:
        raise Http404("Poll does not exist")

    if request.method == 'POST':
        if 'append' in request.POST and request.POST['append'] in ['6m', '12m']:
            logger.info(f"Adding 6/12 months to {username}")
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

                userprofile.favorite_food = userprofile_form.cleaned_data.get("favorite_food")
                userprofile.bookings_allowed = manager_userprofileform.cleaned_data.get("bookings_allowed")
                userprofile.trubadur_member = manager_userprofileform.cleaned_data.get("trubadur_member")
                userprofile.extended_membership_status = manager_userprofileform.cleaned_data.get("extended_membership_status")
                
                if 'date' in request.POST:
                    logger.info(f"Datestring: {request.POST['date']}")
                    date_obj = date.fromisoformat(request.POST['date'])
                    userprofile.application_expiry_date = date_obj

                userprofile.save()

        return redirect('manageUser', username)
    
    else:
        extended_user_form = CustomUserForm(instance=userprofile.user)
        manager_userform = Manageruserform(instance=userprofile.user)
        userprofile_form = UserprofileForm(instance=userprofile)
        manager_userprofileform = ManagerprofileForm(instance=userprofile)

    return render(request, 'updateUser.html', {'currentUser': userprofile, 'extended_user_form': extended_user_form, 'manager_userform': manager_userform, 'userprofile_form': userprofile_form, 'manager_userprofileform': manager_userprofileform, 'unapplied_access': get_unapplied_access(), 'lang': lang})


@staff_member_required
def register_access(request, lang=None):
    changed_userprofiles = list(filter(lambda instance: instance.application_expiry_date != instance.registered_expiry_date, Userprofile.objects.all()))

    if request.method == 'POST':
        if 'reset' in request.POST:
            userprofile = Userprofile.objects.get(user=User.objects.get(username=request.POST['reset']))
            userprofile.application_expiry_date = userprofile.registered_expiry_date
            userprofile.save()
        else:
            # Check if the no-mail checkbox is unticked. In that case, send the mail
            if not 'no-mail' in request.POST:
                logger.info("Sending mail")
                mail = generate_mail(changed_userprofiles)
                send_access_mail(mail)
            else:
                logger.info("Not sending mail as no-mail was checked")
            
            for userprofile in changed_userprofiles:
                userprofile.registered_expiry_date = userprofile.application_expiry_date
                userprofile.save()

        changed_userprofiles = list(filter(lambda instance: instance.application_expiry_date != instance.registered_expiry_date, Userprofile.objects.all()))
    return render(request, 'registerAccess.html', {'changed_userprofiles': changed_userprofiles, 'mail': generate_mail(changed_userprofiles), 'unapplied_access': get_unapplied_access(), 'lang': lang})


def get_unapplied_access():
    return len(list(filter(lambda instance: instance.application_expiry_date != instance.registered_expiry_date, Userprofile.objects.all()))) > 0


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
            body += f"\t{userprofile.user.first_name} {userprofile.user.last_name} ({userprofile.user.username})\n"

    cc = [instance.user.email for instance in userprofiles] if not settings.DEBUG else []
    cc += [FROM_MAIL]
    
    return {
        'from': FROM_MAIL,
        'to': TO_MAIL if not settings.DEBUG else DEBUG_TO_MAIL, 
        'cc': cc, 
        'title': 'Access to frispel', 
        'body': MESSAGE_BODY.format(person='person', body=body)
    }

def get_inactive_users():
    return list(filter(lambda instance: 
        # Change timedelta to 365 when the initial set date is more than one year ago
        instance.registered_expiry_date + timedelta(days=300) <= date.today() and
        not instance.extended_membership_status, 
    Userprofile.objects.all()))


@staff_member_required
def remove_inactive_users(request, lang=None):
    if request.method == 'POST':
        inactive_users = get_inactive_users()
        print(request.POST)
        for userprofile in inactive_users:
            if userprofile.user.username in request.POST:
                userprofile.user.delete()

    inactive_users = get_inactive_users()
    return render(request, 'remove_inactive_users.html', {'inactive_users': inactive_users, 'lang': lang})
