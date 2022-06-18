from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from .models import Voter

class VoterSignUpForm(UserCreationForm):
    mail_addr = forms.CharField(required=True, max_length=60)

    

