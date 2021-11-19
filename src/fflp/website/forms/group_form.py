
from django import forms


class GroupForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=1024 * 16, required=False)


