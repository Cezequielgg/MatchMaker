from django.forms import ModelForm
from django import forms
from .models import Userreg




class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Userreg
        fields = ('image',)