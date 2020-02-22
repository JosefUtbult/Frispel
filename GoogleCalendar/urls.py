from django.contrib import admin
from django.urls import path
from GoogleCalendar import views

urlpatterns = [
	path('', views.calendar, name='calendar'),
]

