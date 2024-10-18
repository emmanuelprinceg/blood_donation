# donations/forms.py

from django import forms
from .models import BloodRequest
from app.models import *

class BloodRequestForm(forms.ModelForm):
    blood_type_needed = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.ChoiceField(choices=CITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = BloodRequest
        fields = ['blood_type_needed', 'location']

class DonorProfileForm(forms.ModelForm):
    blood_type = forms.ChoiceField(choices=BLOOD_GROUP_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.ChoiceField(choices=CITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DonorProfile
        fields = ['blood_type', 'location', 'phone_number']