from django.contrib import admin
from . import models
from django.contrib.auth.models import Group, User

#admin.site.register(models.Candidate)

# to make it unvisible in admin panel
#admin.site.unregister(Group)
#admin.site.unregister(User)


class VoterAdmin(admin.ModelAdmin):

    list_display = ('u_name',)
    fields = ('public_e_sign_key', 'has_voted')
    list_display_links = None
    
    # Disable add permission
    def has_add_permission(self, request):
        return False

    # Disable delete permission
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    

admin.site.register(models.Voter,VoterAdmin)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party','vote_count')

admin.site.register(models.Candidate, CandidateAdmin)