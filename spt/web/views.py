from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from core.workflows.services import WorkFlowService
from spt.models import PermohonanSPT, SPT, SPTLampiran

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