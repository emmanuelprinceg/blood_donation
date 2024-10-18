# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# Predefined choices for blood type and city
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
]

CITY_CHOICES = [
    ('Delhi', 'Delhi'), ('Mumbai', 'Mumbai'), ('Bangalore', 'Bangalore'),
    ('Chennai', 'Chennai'), ('Kolkata', 'Kolkata'), ('Hyderabad', 'Hyderabad'),
    ('Pune', 'Pune'), ('Ahmedabad', 'Ahmedabad')
]


class User(AbstractUser):
    ROLE_CHOICES = [('donor', 'Donor'), ('recipient', 'Recipient')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    location = models.CharField(max_length=100, choices=CITY_CHOICES)
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Added phone number field
    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_type}"

class RecipientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_type_needed = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)  # Dropdown for blood type
    location = models.CharField(max_length=100, choices=CITY_CHOICES)  # Dropdown for cities

    def __str__(self):
        return f"{self.user.username} - {self.blood_type_needed}"
