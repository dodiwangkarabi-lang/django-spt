from django import forms
from spt.models import SPT, PermohonanSPT, SuratPernyataan

class SuratPernyataanForm(forms.ModelForm):
    class Meta:
        model = SuratPernyataan
        fields = ["isi"]

class SPTForm(forms.ModelForm):
    class Meta:
        model = SPT
        fields = "__all__"
        

class PermohonanSPTForm(forms.ModelForm):
    class Meta:
        model = PermohonanSPT
        fields = "__all__"