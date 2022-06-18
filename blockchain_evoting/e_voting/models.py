from distutils.command.upload import upload
from email.policy import default
from django.core.validators import MinValueValidator
from django.db import models
from Crypto import Random
from Crypto.PublicKey import RSA
from sympy import true

class Voter(models.Model):
    RSAkey = RSA.generate(1024)
    public_key = RSAkey.publickey().exportKey()
    private_key = RSAkey.exportKey()
    #print(private_key)

    u_name = models.CharField(max_length=25,primary_key=True)
    mail_addr = models.CharField(max_length=50)
    has_voted = models.BooleanField(default=False,editable=False)
    public_e_sign_key = models.CharField(max_length=350, default= public_key)
    eligibility = models.BooleanField(default=False,editable=True)

class Candidate(models.Model):
    name = models.CharField(max_length=25)
    vote_count = models.IntegerField(default=0,editable=False)
    party = models.CharField(max_length=25)
    #photo = models.ImageField(default='static/vesikalik.jpg',null=True)

class Vote(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE,primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
