"""Content URL Configuration

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
from django.urls import path
from Content import views

urlpatterns = [
    path('lang=<str:lang>', views.home, name='home'),
    path('', views.home, name='home'),
    path('notAMember/lang=<str:lang>', views.notAMember, name='notAMember'),
<<<<<<< HEAD
    path('notAMember/', views.notAMember, name='notAMember'),
    path('becomeAMember/lang=<str:lang>', views.becomeAMember, name='becomeAMember'),
    path('becomeAMember/', views.becomeAMember, name='becomeAMember'),
=======
    path('notAMember', views.notAMember, name='notAMember'),
>>>>>>> 3d8725f (Add english/swedish languages)
]
