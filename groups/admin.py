from django.contrib import admin
from django.db import models as dj_models
from django.forms.widgets import Select

from .models import Family,Company,CompanyInvite,FamilyInvite

admin.site.register(Family)
admin.site.register(Company)
admin.site.register(CompanyInvite)   

admin.site.register(FamilyInvite)




# class CompanyInviteAdmin(admin.ModelAdmin):
#     pass 
#     """code below вырубил всё и засомневался даже в установке allauth"""
    # def status(self, db_field, request, **kwargs):
    #     if db_field.name == "status":
    #         kwargs['choices'] = (
    #             (1, 'Accepted'),
    #             (2 'Rejected'),
    #         )
    #         if request.user.is_superuser:
    #             kwargs['choices'] += (('ready', 'Ready for deployment'),)
    #             print('superuser detected')
    #     return super().formfield_for_choice_field(db_field, request, **kwargs)

     