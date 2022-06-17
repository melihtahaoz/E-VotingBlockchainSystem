from django.db import models

class Voter(models.Model):
    u_name = models.CharField(max_length=25,primary_key=True)
    mail_addr = models.CharField(max_length=50)
    has_voted = models.BooleanField(default=False,editable=False)
    public_e_sign_key = models.CharField(max_length=350, default='test')

class Candidate(models.Model):
    name = models.CharField(max_length=25)
    vote_count = models.IntegerField(default=0,editable=False)
    party = models.CharField(max_length=25)

