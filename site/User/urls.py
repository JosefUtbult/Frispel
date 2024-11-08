"""User URL Configuration

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
from User import views as user_views
import django_cas_ng.views

urlpatterns = [
    path('login/', django_cas_ng.views.LoginView.as_view(), name='cas_ng_login'),
    path('logout/', django_cas_ng.views.LogoutView.as_view(), name='cas_ng_logout'),
    path('redirect/lang=<str:lang>', user_views.redirect, name='redirect'),
    path('redirect/', user_views.redirect, name='redirect'),
    path('account/lang=<str:lang>', user_views.account, name='account'),
    path('account/', user_views.account, name='account'),
    path('account/update/lang=<str:lang>', user_views.updateAccount, name='updateAccount'),
    path('account/update/', user_views.updateAccount, name='updateAccount'),
    path('signup/lang=<str:lang>', user_views.signup, name='signup'),
    path('signup/', user_views.signup, name='signup')
]
