from .models import Thought
from django import forms


class ThoughtForm(forms.ModelForm):
    class Meta:
        model = Thought
        fields = ['score','notes']
