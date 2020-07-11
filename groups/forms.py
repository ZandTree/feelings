from .models import Family,Company,FamilyInvite,CompanyInvite
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class GroupForm(forms.ModelForm):
    class Meta:
        model = None
        fields = ['name','description']


class FamilyForm(GroupForm):
    class Meta(GroupForm.Meta):
        model = Family
        

class CompanyForm(GroupForm):
    class Meta(GroupForm.Meta):
        model = Company


        


class CompanyInviteForm(forms.Form):
    username_or_email = forms.CharField(label="Email or username")

    def clean_username_or_email(self):
        data = self.cleaned_data.get('username_or_email')
        try:
            self.invitee = User.objects.get(Q(username= data)|Q(email=data))
            return data
        except ObjectDoesNotExist:
            return forms.ValidationError("user with this data does not exist")
        
class CompanyLeaveForm(forms.Form):
    """to provide form for post request to be sure that user really wants to leave"""
    pass
     

class FamilyInviteForm(forms.Form):
    username_or_email = forms.CharField(label="Email or username")

    def clean_username_or_email(self):
        data = self.cleaned_data.get('username_or_email')
        try:
            self.invitee = User.objects.get(Q(username= data)|Q(email=data))
            return data
        except ObjectDoesNotExist:
            return forms.ValidationError("user with this data does not exist")
        
class FamilyLeaveForm(forms.Form):
    """to provide form for post request to be sure that user really wants to leave"""
    pass
    
        