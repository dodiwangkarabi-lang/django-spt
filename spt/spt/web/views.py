from django.shortcuts import render, redirect

# messagges
from django.contrib import messages
from django.db import transaction

# forms
from spt.spt.web.forms import (
    SPTForm, SPTFormCreate, SPTFormWithPembuat
)

# models
from workflow.models import Disposisi
from spt.models import (
    SPTStatus, SPT, SPTLampiran
)
from django.contrib.contenttypes.models import ContentType

# services
from spt.spt.services import SPTServices
from notification.services.services import NotificationService

# selectors
from spt.spt.selectors import (
    get_detail
)
from accounts.selectors.selectors import (
    get_pimpinan_user,
    get_kasubag_user,
    get_pegawai_user
)

# constants
from notification.constants.constants import (
    NotificationEventType
)

def review_spt(request, spt_id):
    spt = get_detail(spt_id)
    disposisi = spt.disposisi.first()
    spt_form = SPTForm(instance=spt)
    context = {
        "spt": spt, "disposisi": disposisi,
        "spt_form": spt_form
    }
    return render(request, "spt/spt/pages/review-spt.html", context)

def create_spt(request, disposisi_id):
    
    disposisi = Disposisi.objects.get(id=disposisi_id)
    spt = disposisi.spt
    
    initial = {}
    
    form = SPTFormWithPembuat(request.POST or None, instance=spt)
    # form = SPTFormWithPembuat(request.POST or None, initial=initial)
    
    if request.method == "POST":
        lampiran = request.FILES.getlist("lampiran")
        if not form.is_valid():
            # print("errors")
            # print(form.errors)
            messages.error(request, "Form tidak valid")
            # return redirect("spt:spt_web:create_spt" disposisi.id)
        data = form.cleaned_data
        data["status"] = SPTStatus.DIAJUKAN
        # data["dibuat_oleh"] = request.user
        
        payload = {
            "data": data,
            "disposisi": disposisi,
            "lampiran": lampiran
        }
        
        with transaction.atomic():
        
            # service
            # spt = SPTServices.create_spt_with_disposisi(**payload)
            spt = SPTServices.update_spt_with_disposisi(**payload)
            
            # messages
            # messages.success(request, "SPT berhasil dibuat")
            
            # kirim notifikasi
            # data_notification = {
            #     "pesan": f"SPT: {spt.judul}",
            #     "content_type": ContentType.objects.get_for_model(Disposisi),
            #     "object_id": disposisi.id,
            #     "event_type": NotificationEventType.SPT_CREATED,
            #     "judul": "Pengajuan SPT"
            # }
            
            # NotificationService.kirim_pesan(
            #     pengirim = get_kasubag_user(),
            #     daftar_penerima = [get_pimpinan_user()],
            #     data_notifikasi = data_notification
            # )
        
        return redirect("notification:notification_web:index")
    
    context = {
        "form": form,
        "disposisi": disposisi,
        "pegawai_list": get_pegawai_user(many=True)
    }
    
    return render(request, 'spt/spt/create_spt.html', context)