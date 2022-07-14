from django.contrib import admin
from django.urls import path
from GoogleCalendar import views

urlpatterns = [
	path('lang=<str:lang>', views.calendar, name='calendar'),
	path('', views.calendar, name='calendar'),
]

