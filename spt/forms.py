from django import forms
from django.forms.models import inlineformset_factory
from .models import SPT, SPTLampiran

class SPTForm(forms.ModelForm):
    class Meta:
        model = SPT
        fields = "__all__"
        
class SPTFormRevisi(forms.ModelForm):
    class Meta:
        model = SPT
        fields = ["judul", "deskripsi", "tanggal_mulai", "tanggal_selesai"]
       

class SPTForm2(forms.ModelForm):
    class Meta:
        model = SPT
        fields = ["nomor_spt", "judul", "deskripsi", "tanggal_mulai", "tanggal_selesai"]
         
class SPTLampiranForm(forms.ModelForm):
    class Meta:
        model = SPTLampiran
        fields = ["file", "keterangan"]
        
        # widgets = {
        #     'file': forms.ClearableFileInput(attrs={'multiple': True})
        # }
        
SPTLampiranFormSet = inlineformset_factory(
    SPT, SPTLampiran, 
    form=SPTLampiranForm, extra=1,
    can_delete=True
)