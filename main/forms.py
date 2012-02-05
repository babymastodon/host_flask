from django import forms
from main.models import *

#Make forms here



class UploadForm(forms.Form):
    name = forms.CharField(max_length=20)
    zip_file = forms.FileField()
