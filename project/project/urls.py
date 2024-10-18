"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# blood_donation_platform/urls.py

from django.contrib import admin
from django.urls import path
from app import views as user_views
from donations import views as donation_views
from django.contrib.auth import views as auth_views
from donations import views as donation_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # User Authentication: Sign Up, Log In, and Log Out
    path('signup/', user_views.signup, name='signup'),
    #path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('login/', user_views.custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/logout.html'), name='logout'),

    # Donor-specific: Profile, Dashboard, Accepting Blood Requests
    path('donor/dashboard/', donation_views.donor_dashboard, name='donor_dashboard'),
    path('donor/profile/', user_views.donor_profile, name='donor_profile'),
    path('donor/accept-request/<int:request_id>/', donation_views.accept_blood_request, name='accept_blood_request'),

    # Recipient-specific: Profile, Dashboard, Blood Requests
    #path('recipient/profile/', user_views.recipient_profile, name='recipient_profile'),
    path('recipient/request-blood/', donation_views.create_blood_request, name='create_blood_request'),
    path('recipient/request-blood/<int:donor_id>/', donation_views.request_blood, name='request_blood'),
    #path('recipient/dashboard/', donation_views.donor_dashboard, name='recipient_dashboard'),
    path('recipient/dashboard/', donation_views.recipient_dashboard, name='recipient_dashboard'),
    path('recipient/profile/', user_views.recipient_profile, name='recipient_profile'),
    # Donor dashboard
    path('donor/dashboard/', donation_views.donor_dashboard, name='donor_dashboard'),

    # Recipient dashboard
    path('recipient/dashboard/', donation_views.recipient_dashboard, name='recipient_dashboard'),
]
