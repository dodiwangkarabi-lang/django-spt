from .models import TugasPelaksanaan
from django import forms

class TugasPelaksanaanForm(forms.ModelForm):
    class Meta:
        model = TugasPelaksanaan
        fields = ["keterangan", "hasil", "lampiran"]