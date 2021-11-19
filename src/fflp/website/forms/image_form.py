
from django import forms



class UploaderForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    description = forms.CharField(max_length=1024*16, required=False)
    file = forms.FileField(required=False)

