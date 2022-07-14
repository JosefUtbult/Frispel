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
    path('lang=<str:lang>', views.manager, name='manager'),
    path('', views.manager, name='manager'),
    path('maillist/lang=<str:lang>', views.maillist, name='maillist'),
    path('maillist/', views.maillist, name='maillist'),
    path('trubadur/lang=<str:lang>', views.trubadur, name='trubadur'),
    path('trubadur/', views.trubadur, name='trubadur'),
    path('user/<str:username>/lang=<str:lang>', views.user, name='manageUser'),
    path('user/<str:username>/', views.user, name='manageUser'),
    path('updateUser/<str:username>/lang=<str:lang>', views.updateUser, name='updateUser'),
    path('updateUser/<str:username>/', views.updateUser, name='updateUser'),
    path('users/lang=<str:lang>', views.users, name='manageUsers'),
    path('users/', views.users, name='manageUsers'),
    path('register_access/lang=<str:lang>', views.register_access, name='register_access'),
    path('register_access/', views.register_access, name='register_access'),
<<<<<<< HEAD
    path('remove_inactive_users/', views.remove_inactive_users, name='remove_inactive_users'),
    path('remove_inactive_users/lang=<str:lang>', views.remove_inactive_users, name='remove_inactive_users'),
=======
>>>>>>> 3d8725f (Add english/swedish languages)
]
