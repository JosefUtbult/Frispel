"""Frispel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Manager import views

urlpatterns = [
    path('', views.manager, name='manager'),
    path('maillist', views.maillist, name='maillist'),
    path('trubadur', views.trubadur, name='trubadur'),
    path('user/<str:username>', views.user, name='manageUser'),
    path('updateUser/<str:username>', views.updateUser, name='updateUser'),
    path('users', views.users, name='manageUsers'),
    path('register_access', views.register_access, name='register_access'),
]
