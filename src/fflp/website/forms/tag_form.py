
from django import forms


class TagForm(forms.Form):
    name = forms.CharField(max_length=255, required=True)
    description = forms.CharField(max_length=1024 * 16, required=False)
    parent = forms.ChoiceField(required=False)

