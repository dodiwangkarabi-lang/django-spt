from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

# services
from spt.permohonan.services import PermohonanService

# forms
from spt.permohonan.web.forms import PermohonanForm

# selectors
from spt.permohonan.selectors import (
    get_permohonan_by_id,
    get_lampiran_permohonan
)

def index(request):
    context = {}
    return render(request, 'spt/permohonan/list.html', context)

def detail(request, permohonan_id):
    permohonan = get_permohonan_by_id(permohonan_id)
    daftar_lampiran = get_lampiran_permohonan(permohonan_id)
    context = {
        "permohonan": permohonan,
        "daftar_lampiran": daftar_lampiran
    }
    return render(request, 'spt/permohonan/detail.html', context)

@login_required
def create(request):
    form = PermohonanForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        data_permohonan = form.cleaned_data
        data_permohonan["dibuat_oleh"] = request.user
        daftar_lampiran = request.FILES.getlist('lampiran')
        keterangan = request.POST.getlist('keterangan')
        
        daftar_lampiran = [
            {
                "file": item,
                "keterangan": keterangan[i]
            }
            for i, item in enumerate(daftar_lampiran)
        ]
        
        permohonan = PermohonanService.create_permohonan_with_lampiran(data_permohonan, daftar_lampiran)
        return redirect("spt_permohonan_detail", permohonan_id=permohonan.id)
    return render(request, 'spt/permohonan/create.html')