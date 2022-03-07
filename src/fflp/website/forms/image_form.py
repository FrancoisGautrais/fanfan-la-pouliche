
from django import forms

from website.fields.fields import ListStrField


class UploaderForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    description = forms.CharField(max_length=1024*16, required=False)
    file = forms.FileField(required=False)
    tags = ListStrField(required=False)



class UploaderCodeForm(forms.Form):
    code = forms.CharField(max_length=256, required=False)
    comment = forms.CharField(max_length=1024*16, required=False)
    file = forms.FileField(required=False)



