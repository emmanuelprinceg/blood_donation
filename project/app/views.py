# app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserSignUpForm, DonorProfileForm, RecipientProfileForm
from .models import *
from django.contrib.auth.decorators import login_required
def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            if user.role == 'donor':
                return redirect('donor_profile')
            else:
                return redirect('recipient_profile')
    else:
        form = UserSignUpForm()
    
    return render(request, 'app/signup.html', {'form': form})

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on the user role
                if user.role == 'donor':
                    return redirect('donor_dashboard')
                elif user.role == 'recipient':
                    return redirect('recipient_dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'app/login.html', {'form': form})

@login_required
def donor_profile(request):
    try:
        # Try to get the donor profile if it exists
        donor_profile = request.user.donorprofile
    except DonorProfile.DoesNotExist:
        donor_profile = None

    if request.method == 'POST':
        # Handle form submission
        form = DonorProfileForm(request.POST, instance=donor_profile)
        if form.is_valid():
            donor_profile = form.save(commit=False)
            donor_profile.user = request.user  # Assign the profile to the logged-in user
            donor_profile.save()
            return redirect('donor_dashboard')
    else:
        # Display the form with existing donor profile data (if any)
        form = DonorProfileForm(instance=donor_profile)

    return render(request, 'app/donor_profile.html', {'form': form})
@login_required
def recipient_profile(request):
    # Ensure the user is a recipient
    if request.user.role != 'recipient':
        return redirect('donor_dashboard')

    try:
        # Try to get the recipient profile if it exists
        recipient_profile = request.user.recipientprofile
    except RecipientProfile.DoesNotExist:
        recipient_profile = None

    if request.method == 'POST':
        form = RecipientProfileForm(request.POST, instance=recipient_profile)
        if form.is_valid():
            recipient_profile = form.save(commit=False)
            recipient_profile.user = request.user
            recipient_profile.save()
            return redirect('recipient_dashboard')
    else:
        form = RecipientProfileForm(instance=recipient_profile)

    return render(request, 'app/recipient_profile.html', {'form': form})
