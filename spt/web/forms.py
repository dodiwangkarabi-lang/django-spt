from django import forms
from spt.models import SPT, PermohonanSPT

class SPTForm(forms.ModelForm):
    class Meta:
        model = SPT
        fields = "__all__"
        

class PermohonanSPTForm(forms.ModelForm):
    class Meta:
        model = PermohonanSPT
        fields = "__all__"