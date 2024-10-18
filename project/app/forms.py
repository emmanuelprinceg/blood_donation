# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class DonorProfileForm(forms.ModelForm):
    blood_type = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.ChoiceField(choices=CITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DonorProfile
        fields = ['blood_type', 'location', 'phone_number']

class RecipientProfileForm(forms.ModelForm):
    blood_type_needed = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.ChoiceField(choices=CITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = RecipientProfile
        fields = ['blood_type_needed', 'location']
