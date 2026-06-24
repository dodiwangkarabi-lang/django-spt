from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse
from spt.forms import SPTForm, SPTFormRevisi
from spt.models import SPT, SPTLampiran, SPTStatus, PermohonanSPT
from spt.services_old import *
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
#     get_user_role,
#     get_permohonan_for_user
# )

# timezone
from django.utils import timezone

from accounts.models import Profile
from accounts.forms import UserUpdateForm

# forms
from tugas.forms import TugasPelaksanaanForm

# models
from tugas.models import TugasPelaksanaan
from spt.models import SPTStatus

from tugas.services import upload_laporan_service, is_laporan_exist

from core.decorators import roles_required

# import Q untuk filter
from django.db.models import Q, Value, CharField, F
from django.db.models.functions import Concat

# selectors
from spt.spt.selectors import (
    get_spt, get_spt_by_user, get_spt_by_role
)

from django.core.paginator import Paginator

@login_required
def accounts_profile(request):
    profile = Profile.objects.get(user=request.user)
    context = {"profile": profile}
    return render(request, "pages/pegawai/profile.html", context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts_profile")
    else:
        form = UserUpdateForm(instance=request.user)

    context = {"form": form}
    return render(request, "pages/pegawai/edit-profile.html", context)

# @login_required
def index(request):
    user = request.user
    
    if not user.is_authenticated:
        return redirect("core_login")
    
    # cek group
    if user.groups.filter(name="pimpinan").exists():
        return redirect("core_pimpinan_dashboard")

    elif user.groups.filter(name="kasubag").exists():
        return redirect("core_kasubag_dashboard")

    elif user.groups.filter(name="pegawai").exists():
        return redirect("core_pegawai_dashboard")
    
    # return render(request, "core/index.html")


def dashboard(request):
    return render(request, "core/dashboard.html")

@login_required
# @roles_required("pegawai")
def permohonan_list_htmx(request):
    init = request.GET.get("init", "")
    q = request.GET.get("q", "")
    tanggal = request.GET.get("tanggal", "")
    page_number = request.GET.get("page")
    
    # spt_list = get_spt_list(request.user).order_by("-created_at").filter(
    #     Q(status=SPTStatus.DIAJUKAN) |
    #     Q(status=SPTStatus.DRAFT) |
    #     Q(status=SPTStatus.REVISI_KASUBAG) |
    #     Q(status=SPTStatus.DITOLAK_KASUBAG) |
    #     Q(status=SPTStatus.DITOLAK_PIMPINAN) |
    #     Q(status=SPTStatus.PERMOHONAN_DIAJUKAN) |
    #     Q(status=SPTStatus.REVIEW_KASUBAG)
    # )
    
    spt_list = get_permohonan_for_user(request.user)
    # spt_list = get_spt_list(request.user).order_by("-created_at")
    
    if q:
        spt_list = spt_list.filter(Q(nomor_spt__icontains=q) | Q(judul__icontains=q))
    
    if tanggal:
        spt_list = spt_list.filter(created_at__date=tanggal)
        
    # qs = spt_list
    qs = spt_list.select_related("permohonan_spt").filter(permohonan_spt__isnull=False)\
        .annotate(
            status_permohonan=F("permohonan_spt__status"),
            id_permohonan=F("permohonan_spt__id"),
        )
        
    # print(qs)
    
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page_number)
    
    columns = [
        # {"key": "nomor_spt", "label": "Nomor SPT"},
        {"key": "judul", "label": "Judul"},
        {"key": "created_at", "label": "Tanggal", "tipe": "date"},
        {"key": "status_permohonan", "label": "Status"},
    ]
    
    role = get_user_role(request.user)
    actions = [
            {"key": "detail", "label": "Detail", "url": "permohonan_detail", "param": "id"},
    ]
    
    if role == "pegawai":
        actions = [
            {"key": "detail", "label": "Detail", "url": "permohonan_detail", "param": "id"},
            # {"key": "upload", "label": "Upload Laporan", "url": "core_upload_laporan", "param": "id"},
            {"key": "delete", "label": "Hapus", "url": "core_permohonan_spt_delete", "param": "id"},
        ]
    

    context = {
        "page_obj": page_obj,
        "columns": columns,
        "actions": actions,
        "current_url": "permohonan_list_htmx",
        # "detail_url": "core_spt_detail",
        # "upload_url": "core_upload_laporan",
        "judul_halaman": "Daftar Permohonan SPT",
    }
    
    if init:
        return render(request, "partials/permohonan-spt-list.html", context)
    
    return render(request, "partials/_tabel.html", context)

def permohonan_list(request):
    # permohonan_list = PermohonanSPT.objects.all()
    
    context = {
        # "permohonan_list": permohonan_list
    }
    return render(request, "pages/core/permohonan.html", context)

def permohonan_detail(request, id):
    spt = SPT.objects.get(id=id)
    permohonan = spt.permohonan_spt
    
    # spt = permohonan.spt
    context = {
        "spt": spt,
        "SPTStatus": SPTStatus,
        "permohonan": permohonan,
        "can_process": spt.status in [SPTStatus.DRAFT, SPTStatus.REVISI_KASUBAG]
    }
    return render(request, "pages/core/permohonan-detail.html", context)

def disposisi_list(request):
    return render(request, "pages/core/disposisi-list.html")

def spt_list(request):
    return render(request, "pages/core/spt-list.html")

@login_required
# @roles_required("kasubag")
def disposisi_detail(request, disposisi_id):
    disposisi = get_disposisi_detail(disposisi_id, request.user)
    context = {"disposisi": disposisi}
    return render(request, "pages/kasubag/disposisi-detail.html", context)

@login_required
# @roles_required("pegawai")
def spt_detail(request, spt_id):
    # spt = get_spt_detail(spt_id, request.user)
    spt = SPTService.get_detail_for_user(request.user, spt_id)
    tugas_pelaksanaan_list = spt.tugas.all()
    
    for tugas in tugas_pelaksanaan_list:
        tugas.is_surat_pernyataan_tugas = hasattr(tugas, "surat_pernyataan_tugas")
    
    lampiran_list = spt.lampiran.all()
    context = {
        "spt": spt,
        "lampiran_list": lampiran_list,
        "tugas_pelaksanaan_list": tugas_pelaksanaan_list
    }

    return render(request, "pages/core/spt-detail.html", context)

@login_required
# @roles_required("pegawai")
def spt_list_htmx(request):
    init = request.GET.get("init", "")
    q = request.GET.get("q", "")
    tanggal = request.GET.get("tanggal", "")
    page_number = request.GET.get("page")
    
    role = get_user_role(request.user)
    
    # spt_list = get_spt_list(request.user).order_by("-created_at").filter(
    #     Q(status=SPTStatus.DIAJUKAN) |
    #     Q(status=SPTStatus.DRAFT) |
    #     Q(status=SPTStatus.REVISI_KASUBAG) |
    #     Q(status=SPTStatus.DITOLAK_KASUBAG) |
    #     Q(status=SPTStatus.DITOLAK_PIMPINAN) |
    #     Q(status=SPTStatus.PERMOHONAN_DIAJUKAN) |
    #     Q(status=SPTStatus.REVIEW_KASUBAG)
    # ) # permohonan
    
    # spt_list = SPTService.get_for_user(request.user)
    # spt_list = get_spt_for_user(request.user)
    
    spt_list = get_spt_by_role(request.user)
    # spt_list = get_spt()
    
    # spt_list = get_spt_list(request.user).order_by("-created_at")
    
    if q:
        spt_list = spt_list.filter(Q(nomor_spt__icontains=q) | Q(judul__icontains=q))
    
    if tanggal:
        spt_list = spt_list.filter(created_at__date=tanggal)
    
    spt_list = spt_list.order_by("-created_at")
    paginator = Paginator(spt_list, 10)
    page_obj = paginator.get_page(page_number)
    
    columns = [
        # {"key": "nomor_spt", "label": "Nomor SPT"},
        {"key": "judul", "label": "Judul"},
        {"key": "created_at", "label": "Tanggal", "tipe": "date"},
        {"key": "status", "label": "Status"},
    ]
    
    actions = [
        {"key": "detail", "label": "Detail", "url": "spt_detail", "param": "spt_id"},
    ]
    if role == "pegawai":
        actions = [
            {"key": "detail", "label": "Detail", "url": "core_spt_detail", "param": "spt_id"},
            {"key": "upload", "label": "Upload Laporan", "url": "core_upload_laporan", "param": "spt_id"},
        ]
    

    context = {
        "page_obj": page_obj,
        "columns": columns,
        "actions": actions,
        "current_url": "pegawai_spt_list_htmx",
        # "detail_url": "core_spt_detail",
        # "upload_url": "core_upload_laporan",
        # "judul_halaman": "Daftar Permohonan SPT",
    }
    
    if init:
        return render(request, "partials/spt-list.html", context)
    
    return render(request, "partials/_tabel-spt.html", context)