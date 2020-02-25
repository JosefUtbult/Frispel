from django.shortcuts import render

def home(request):
	return render(request, 'home.html')

def notAMember(request):
	return render(request, 'notAMember.html')