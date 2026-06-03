from django import forms
from spt.models import SPT

class SPTForm(forms.ModelForm):
    class Meta:
        model = SPT
        fields = "__all__"