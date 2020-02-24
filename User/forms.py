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

	ltu_id = forms.CharField(label='LTU-ID', max_length=100, required=False, help_text="This is required for access into Frispel. If you don't have an LTU ID, leave this blank and contact the chairman of Frispel for more information.")
	favorite_food = forms.CharField(label='Favorite food', max_length=100, required=True)
	trubadur_member = forms.BooleanField(label='Are you a member of Trubadur?', required=False)

	class Meta:
		model = Userprofile
		fields = ('ltu_id', 'trubadur_member', 'favorite_food')

class Manageruserform(forms.ModelForm):

	is_staff = forms.BooleanField(label='Manager privileges')

	class Meta:
		model = User
		fields = ('is_staff',)


class ManagerprofileForm(forms.ModelForm):

	extended_membership_status = forms.IntegerField(label='Extended Membership')
	expiry_date = forms.DateField(label='Membership expiry date')

	class Meta:
		model = Userprofile
		fields = ('extended_membership_status', 'expiry_date')
