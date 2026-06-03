from django import forms

# models
from spt.models import (
    PermohonanSPT, LampiranPermohonanSPT
)

class PermohonanForm(forms.ModelForm):
    class Meta:
        model = PermohonanSPT
        fields = "__all__"
        
class LampiranPermohonanForm(forms.ModelForm):
    class Meta:
        model = LampiranPermohonanSPT
        fields = "__all__"