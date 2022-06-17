from django.contrib import admin
from . import models

#admin.site.register(models.Candidate)





class VoterAdmin(admin.ModelAdmin):

    list_display = ('public_e_sign_key', 'has_voted')

    # Disable add permission
    def has_add_permission(self, request):
        return False

    # Disable delete permission
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(models.Voter,VoterAdmin)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party','vote_count')

admin.site.register(models.Candidate, CandidateAdmin)