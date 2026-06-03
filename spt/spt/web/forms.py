from django import forms

# models
from spt.models import SPT, SPTLampiran

class SPTForm(forms.ModelForm):
    class Meta:
        model = SPT
        fields = "__all__"
        
class SPTFormCreate(forms.ModelForm):
    class Meta:
        model = SPT
        fields = ["judul", "deskripsi", "tanggal_mulai", "tanggal_selesai"]
        
class SPTFormWithPembuat(forms.ModelForm):
    class Meta:
        model = SPT
        fields = ["judul", "deskripsi", "tanggal_mulai", "tanggal_selesai", "dibuat_oleh"]