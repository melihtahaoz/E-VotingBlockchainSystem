from distutils.command.upload import upload
from email.policy import default
from django.core.validators import MinValueValidator
from django.db import models
from Crypto import Random
from Crypto.PublicKey import RSA

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

