from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile


class CustomUserForm(forms.ModelForm):

	first_name = forms.CharField(label='First name', max_length=100, required=True)
	last_name = forms.CharField(label='Last name', max_length=100, required=True)
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email',)


class UserprofileForm(forms.ModelForm):

	favorite_food = forms.CharField(label='Favorite food', max_length=100, required=True)

	class Meta:
		model = Userprofile
		fields = ('favorite_food',)

class Manageruserform(forms.ModelForm):

	is_staff = forms.BooleanField(label='Manager privileges', required=False, 
		help_text='Give user access to the Manager page and the Users page.')

	class Meta:
		model = User
		fields = ('is_staff',)


class ManagerprofileForm(forms.ModelForm):

	bookings_allowed = forms.IntegerField(label='Number of bookings allowed')
	trubadur_member = forms.BooleanField(label='Trubadur Member', required=False)
	extended_membership_status = forms.BooleanField(label='Extended Membership', required=False, 
		help_text='Extend membership indefinitely, disabling the expiry date.')

	class Meta:
		model = Userprofile
		fields = ('bookings_allowed', 'trubadur_member', 'extended_membership_status')
