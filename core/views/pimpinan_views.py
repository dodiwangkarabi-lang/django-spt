from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse
from spt.forms import SPTForm, SPTFormRevisi
from spt.models import SPT, SPTLampiran, SPTStatus
from spt.services import *
# from spt.services import (
#     create_spt,
#     get_spt_list,
#     get_spt_detail,
#     get_inbox_disposisi,
#     get_disposisi_detail,
#     kasubbag_approve,
#     kasubbag_reject,
#     kasubbag_revisi,
#     kasubbag_terima_spt,
#     kasubbag_review,
#     update_draft_spt_kasubag,
#     pimpinan_approve,
#     pimpinan_reject,
#     pimpinan_revisi,
#     update_draft_spt,
#     simpan_draft_spt,
#     submit_spt,
#     upload_lampiran_spt,
#     delete_lampiran_spt,
#     get_lampiran_spt_detail,
#     get_lampiran_spt_list,
#     buat_spt,
#     get_spt_diterima_list,
#     get_kasubag_user,
#     get_pimpinan_user,
#     pimpinan_setujui_permohonan,
#     update_dan_create_disposisi_baru,
# )

# utils
from core.utils import update_by_action

# timezone
from django.utils import timezone

from accounts.models import Profile
from accounts.forms import UserUpdateForm

from tugas.forms import TugasPelaksanaanForm
from tugas.models import TugasPelaksanaan
from tugas.services import upload_laporan_service, is_laporan_exist

from core.decorators import roles_required
from django.core.paginator import Paginator

from django.db.models import Q

# analisis
from spt.analisis_services import RangkumanSPT

# -------------------------------------------pimpinan htmx--------------------------------

@login_required
@roles_required("pimpinan")
def laporan_perjalanan_dinas_htmx(request):
    init = request.GET.get("init", "")
    q = request.GET.get("q", "")
    tanggal = request.GET.get("tanggal", "")
    page_number = request.GET.get("page")
    
    qs = TugasPelaksanaan.objects.all().order_by("-created_at")
    
    
    
    if q:
        qs = qs.filter(
            Q(spt__nomor_spt__icontains=q) | 
            Q(spt__judul__icontains=q)
        )
    
    if tanggal:
        qs = qs.filter(created_at__date=tanggal)
        
    for obj in qs:
        obj.nomor_spt = obj.spt.nomor_spt
        obj.pembuat_spt = obj.spt.dibuat_oleh.profile.nama
    
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page_number)
    
    columns = [
        {"key": "nomor_spt", "label": "Nomor SPT"},
        {"key": "pembuat_spt", "label": "Pengaju"},
        {"key": "created_at", "label": "Tanggal", "tipe": "date"},  
    ]
    
    actions = [
        {"key": "detail", "label": "Detail", "url": "core_pimpinan_laporan_detail_pimpinan", "param": "spt_id"},
        {"key": "upload", "label": "Upload Laporan", "url": "core_upload_laporan", "param": "spt_id"},
    ]
    

    context = {
        "page_obj": page_obj,
        "columns": columns,
        "actions": actions,
        "current_url": "pimpinan_laporan_perjalanan_dinas_htmx", # nama route
    }
    
    if init:
        return render(request, "partials/spt-list.html", context)
    
    return render(request, "partials/_tabel-spt.html", context)

# -------------------------------------------pimpinan--------------------------------
@login_required
@roles_required("pimpinan")
def laporan_detail_pimpinan(request, laporan_id):
    laporan = TugasPelaksanaan.objects.get(id=laporan_id)
    context = {"laporan": laporan}
    return render(request, "pages/pimpinan/laporan-detail-pimpinan.html", context)

@login_required
@roles_required("pimpinan")
def laporan_pelaksanaan(request):
    laporan_list = TugasPelaksanaan.objects.all().order_by("-created_at")
    context = {"laporan_list": laporan_list}
    return render(request, "pages/pimpinan/laporan-pelaksanaan.html", context)

@login_required
@roles_required("pimpinan")
def pimpinan(request):
    rangkuman = RangkumanSPT()
    context = {
       "total_spt": rangkuman.total_spt(),
       "total_spt_disetujui": rangkuman.total_spt_disetujui(),
       "total_laporan_selesai": rangkuman.total_laporan_selesai()
    }
    return render(request, "pages/pimpinan/dashboard-pimpinan.html", context)

@login_required
@roles_required("pimpinan")
def disposisi_pimpinan(request):
    disposisi_list = get_inbox_disposisi(request.user)
    # print(disposisi_list)
    context = {"disposisi_list": disposisi_list}
    return render(request, "pages/pimpinan/disposisi.html", context)

@login_required
@roles_required("pimpinan")
def disposisi_detail_pimpinan(request, disposisi_id):
    disposisi = get_disposisi_detail(disposisi_id, request.user)
    context = {"disposisi": disposisi}
    return render(request, "pages/pimpinan/disposisi-detail.html", context)

@login_required
@roles_required("pimpinan")
def approval_final(request):
    return render(request, "pages/pimpinan/approval-final.html")

@login_required
@roles_required("pimpinan")
def ttd(request):
    return render(request, "pages/pimpinan/ttd.html")

@login_required
@roles_required("pimpinan")
def pimpinan_setujui_permohonan_view(request, disposisi_id):
    disposisi = get_disposisi_detail(disposisi_id, request.user)
    if request.method == "POST":
        pimpinan = get_pimpinan_user()
        kasubag = get_kasubag_user()

        catatan = "Permohonan disetujui oleh pimpinan"
        disposisi_baru = pimpinan_setujui_permohonan(
            disposisi, pimpinan, kasubag, catatan
        )
        
        # tambahan
        # spt = update_by_action(
        #     disposisi.spt, action="setujui_permohonan_oleh_pimpinan"
        #     # dari_user=request.user, ke_user=ke_user
        # )

        return redirect("core_pimpinan_disposisi")
    else:
        context = {"disposisi": disposisi}
        return render(request, "pages/kasubag/approval.html", context)

# disetujui_final
@login_required
@roles_required("pimpinan")
def approve_pimpinan(request, disposisi_id):
    if request.method == "POST":
        disposisi = get_disposisi_detail(disposisi_id, request.user)
        spt = pimpinan_approve(disposisi, request.user)
        return redirect("core_pimpinan_disposisi")
    else:
        context = {"disposisi": disposisi}
        return render(request, "pages/kasubag/approval.html", context)

@login_required
@roles_required("pimpinan")
def reject_pimpinan(request, disposisi_id):
    if request.method == "POST":
        catatan = request.POST["catatan"]
        disposisi = get_disposisi_detail(disposisi_id, request.user)

        spt = pimpinan_reject(disposisi, request.user, catatan=catatan)
        return redirect("core_pimpinan_disposisi")

    else:
        return render(request, "pages/pimpinan/reject.html")

@login_required
@roles_required("pimpinan")
def revisi_pimpinan(request, disposisi_id):
    if request.method == "POST":
        pimpinan = User.objects.filter(groups__name="pimpinan").first()
        pegawai_id = request.POST["pegawai_id"]
        catatan = request.POST.get("catatan", "")
        disposisi = get_disposisi_detail(disposisi_id, request.user)
        kasubag_user = User.objects.get(id=pegawai_id)

        pimpinan_revisi(disposisi, pimpinan, penerima=kasubag_user, catatan=catatan)
        return redirect("core_pimpinan_disposisi")

    return render(request, "pages/pimpinan/revisi.html")