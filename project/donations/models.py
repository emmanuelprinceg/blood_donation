from django.db import models

# Create your models here.
# donations/models.py

from django.db import models
from app.models import DonorProfile, RecipientProfile
from django.utils import timezone

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting for Response'),
        ('accepted', 'Accepted'),
        ('fulfilled', 'Fulfilled'),
    ]

    recipient = models.ForeignKey(RecipientProfile, on_delete=models.CASCADE)
    donor = models.ForeignKey(DonorProfile, on_delete=models.SET_NULL, null=True, blank=True)  # Donor accepting the request
    blood_type_needed = models.CharField(max_length=3)
    location = models.CharField(max_length=100)
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"Blood request by {self.recipient.user.username}"

class DonationAcceptance(models.Model):
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE)
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
    accepted_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Request {self.blood_request.id} accepted by {self.donor.user.username}"
