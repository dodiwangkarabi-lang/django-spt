from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.conf import settings

from core.workflows.services import WorkFlowService
from spt.models import PermohonanSPT, SPT, SPTLampiran, SuratPernyataan

# forms
from .forms import SuratPernyataanForm

# messages
from django.contrib import messages
# from django.template import Template, Context
from django.template.loader import render_to_string

def cetak_surat_pernyataan(request, surat_pernyataan_id):
    surat_pernyataan = get_object_or_404(SuratPernyataan, id=surat_pernyataan_id)
    
    kop_surat = settings.MEDIA_URL + "lainnya/kop_surat.png"
    context = {
        "surat_pernyataan": surat_pernyataan,
        "kop_surat": kop_surat
    }
    return render(request, "spt/spt/pages/cetak-surat-pernyataan.html", context)

def surat_pernyataan(request, spt_id):
    form = SuratPernyataanForm(request.POST or None)
    spt = get_object_or_404(SPT, id=spt_id)
    
    if spt.has_surat_pernyataan:
        content_html = spt.surat_pernyataan.isi
        surat_pernyataan = spt.surat_pernyataan
    else:
        data_template = {
            "nama" : spt.dibuat_oleh.profile.nama,
            "nip": spt.dibuat_oleh.profile.nip,
            "pangkat": spt.dibuat_oleh.profile.pangkat,
            "unit_kerja": spt.dibuat_oleh.profile.unit_kerja,
            
            "nomor_spt": spt.nomor_spt,
            "tanggal_mulai": spt.tanggal_mulai,
            "tanggal_selesai": spt.tanggal_selesai
        }
        content_html = render_to_string(
            "spt/spt/partials/surat-pernyataan-template.html",
            data_template
        )
        
        surat_pernyataan = None
       
    
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            # update or create
            surat_pernyataan, created = SuratPernyataan.objects.get_or_create(spt=spt)
            surat_pernyataan.isi = data.get("isi")
            surat_pernyataan.save()
                        
            return redirect("spt:surat_pernyataan", spt_id=spt_id)
        else:
            messages.error(request, form.errors)    
            
    context = {
        "form": form,
        "surat_pernyataan": surat_pernyataan, 
        "content_html": content_html
    }
    return render(request, "spt/spt/pages/surat-pernyataan.html", context)

def permohonan_create(request):
    service_spt = WorkFlowService(SPT)
    service_permohonan = WorkFlowService(PermohonanSPT)
    
    if request.method == "POST":
        data = request.POST.copy()
        lampiran = request.FILES.getlist("lampiran")
        
        with transaction.atomic():
            # buat spt
            spt = SPT.objects.create(
                nomor_spt=data.get("nomor_spt"),
                judul=data.get("judul"),
                deskripsi=data.get("deskripsi"),
                tanggal_mulai=data.get("tanggal_mulai"),
                tanggal_selesai=data.get("tanggal_selesai"),
                dibuat_oleh=request.user,
                status="draft",
            )
            spt.save()
            
            # buat permohonan
            permohonan_spt = PermohonanSPT(
                spt=spt,
                tujuan=data.get("tujuan"),
                tanggal=data.get("tanggal"),
                dibuat_oleh=request.user,
                status="draft"
            )
            permohonan_spt.save()
            
            def upload_lampiran_spt(spt_id, data): # spt -> Lampiran (1:N)
                """keterangan

                Args:
                    spt_id (str): id dari spt
                    data (any): data utama

                Returns:
                    lampiran: instance object dari Lampiran
                """
                spt = get_object_or_404(SPT, id=spt_id)
                lampiran = SPTLampiran.objects.create(
                    spt=spt,
                    file=data.get("file"),
                    keterangan=data.get("keterangan")
                )
                return lampiran
            
            # buat lampiran
            if lampiran:
                for lamp in lampiran:
                    data_lampiran = {
                        "file": lamp,
                        "keterangan": data.get("keterangan", ""),
                    }
                    upload_lampiran_spt(spt.id, data_lampiran)
                    
            
            return redirect("core_spt_detail", spt_id=spt.id)
    
    context = {}
    return render(request, "spt/permohonan/create.html", context)