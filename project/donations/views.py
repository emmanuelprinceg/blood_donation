from django.shortcuts import render

# Create your views here.
# donations/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BloodRequest, DonationAcceptance
from app.models import DonorProfile, RecipientProfile
from .forms import BloodRequestForm

@login_required
def create_blood_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.recipient = request.user.recipientprofile
            blood_request.save()
            return redirect('recipient_dashboard')
    else:
        form = BloodRequestForm()
    return render(request, 'donations/create_blood_request.html', {'form': form})

@login_required
def donor_dashboard(request):
    # Ensure the user is a donor
    if request.user.role != 'donor':
        return redirect('recipient_dashboard')

    try:
        # Get the logged-in donor's profile
        donor_profile = request.user.donorprofile
    except DonorProfile.DoesNotExist:
        return redirect('donor_profile')

    # Query for blood requests assigned to this donor and that are still 'waiting'
    blood_requests = BloodRequest.objects.filter(donor=donor_profile, status='waiting')

    return render(request, 'donations/donor_dashboard.html', {
        'blood_requests': blood_requests
    })

@login_required
def accept_blood_request(request, request_id):
    # Ensure the user is a donor
    if request.user.role != 'donor':
        return redirect('recipient_dashboard')

    try:
        # Get the donor profile
        donor_profile = request.user.donorprofile
    except DonorProfile.DoesNotExist:
        return redirect('donor_profile')

    # Get the blood request
    blood_request = get_object_or_404(BloodRequest, id=request_id, status='waiting')

    # Update the request with the donor's details and change status to 'accepted'
    blood_request.donor = donor_profile
    blood_request.status = 'accepted'
    blood_request.save()

    return redirect('donor_dashboard')
@login_required
def recipient_dashboard(request):
    # Ensure the user is a recipient
    if request.user.role != 'recipient':
        return redirect('donor_dashboard')

    try:
        # Get the recipient profile
        recipient_profile = request.user.recipientprofile
    except RecipientProfile.DoesNotExist:
        return redirect('recipient_profile')

    # Get available donors in the same location
    available_donors = DonorProfile.objects.filter(location=recipient_profile.location)

    # Prepare data to indicate if a request has been made by the recipient for each donor
    donor_requests = []
    for donor in available_donors:
        # Check if a request from the recipient exists for the donor
        blood_request = BloodRequest.objects.filter(recipient=recipient_profile, donor=donor, fulfilled=False).first()
        donor_requests.append({
            'donor': donor,
            'request_exists': bool(blood_request),
            'blood_request': blood_request  # Pass the blood request if it exists
        })

    return render(request, 'donations/recipient_dashboard.html', {
        'donor_requests': donor_requests,
    })


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.models import DonorProfile
@login_required
def request_blood(request, donor_id):
    # Ensure the user is a recipient
    if request.user.role != 'recipient':
        return redirect('donor_dashboard')

    try:
        # Get the recipient profile
        recipient_profile = request.user.recipientprofile
    except RecipientProfile.DoesNotExist:
        return redirect('recipient_profile')

    # Get the donor profile using the donor_id
    donor_profile = get_object_or_404(DonorProfile, user_id=donor_id)

    # Check if a request from this recipient to this donor already exists
    existing_request = BloodRequest.objects.filter(recipient=recipient_profile, donor=donor_profile, fulfilled=False).exists()

    if existing_request:
        # If the request already exists, prevent creating another one
        return redirect('recipient_dashboard')

    # Create a new blood request if none exists
    blood_request = BloodRequest.objects.create(
        recipient=recipient_profile,
        donor=donor_profile,
        blood_type_needed=recipient_profile.blood_type_needed,
        location=recipient_profile.location,
        status='waiting',
        fulfilled=False
    )

    return redirect('recipient_dashboard')