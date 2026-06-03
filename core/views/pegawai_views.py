from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse
from spt.forms import SPTForm, SPTFormRevisi
from spt.models import SPT, SPTLampiran, SPTStatus
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
#     get_spt_for_user
# )

# timezone
from django.utils import timezone
from datetime import date

from accounts.models import Profile
from accounts.forms import UserUpdateForm

from tugas.forms import TugasPelaksanaanForm
from tugas.models import TugasPelaksanaan
from tugas.services import upload_laporan_service, is_laporan_exist

from core.decorators import roles_required

# import Q untuk filter
from django.db.models import Q, Value, CharField, F
from django.db.models.functions import Concat

from django.core.paginator import Paginator

# utils
from core.utils import update_by_action

# selectors
from spt.spt.selectors import (
    get_spt, get_spt_by_user, get_spt_by_role
)

# -------------------------------------------pegawai htmx --------------------------------
@login_required
@roles_required("pegawai")
def grid_card_htmx(request):
    spt_list = get_spt_list(request.user).order_by("-created_at")
    
    diajukan = spt_list.filter(status="diajukan").count()
    selesai = spt_list.filter(status="selesai").count()
    permohonan_diterima = spt_list.filter(Q(status="disetujui_final") | Q(status="selesai")).count()
    selesai_dilaksanakan = spt_list.filter(status="selesai").count()
    context = {
        "spt_list": spt_list,
        "total_spt": spt_list.count(),
        "diajukan": diajukan,
        "selesai": selesai,
        "selesai_dilaksanakan": selesai_dilaksanakan,
        "permohonan_diterima": permohonan_diterima
    }
    return render(request, "partials/grid-card.html", context)


# @login_required
# # @roles_required("pegawai")
# def spt_list_htmx(request):
#     init = request.GET.get("init", "")
#     q = request.GET.get("q", "")
#     tanggal = request.GET.get("tanggal", "")
#     page_number = request.GET.get("page")
    
#     # spt_list = get_spt_list(request.user).order_by("-created_at").filter(
#     #     Q(status=SPTStatus.DIAJUKAN) |
#     #     Q(status=SPTStatus.DRAFT) |
#     #     Q(status=SPTStatus.REVISI_KASUBAG) |
#     #     Q(status=SPTStatus.DITOLAK_KASUBAG) |
#     #     Q(status=SPTStatus.DITOLAK_PIMPINAN) |
#     #     Q(status=SPTStatus.PERMOHONAN_DIAJUKAN) |
#     #     Q(status=SPTStatus.REVIEW_KASUBAG)
#     # ) # permohonan
    
#     spt_list = SPTService.get_for_user(request.user)
#     # spt_list = get_spt_for_user(request.user)
    
#     # spt_list = get_spt_list(request.user).order_by("-created_at")
    
#     if q:
#         spt_list = spt_list.filter(Q(nomor_spt__icontains=q) | Q(judul__icontains=q))
    
#     if tanggal:
#         spt_list = spt_list.filter(created_at__date=tanggal)
    
#     paginator = Paginator(spt_list, 10)
#     page_obj = paginator.get_page(page_number)
    
#     columns = [
#         # {"key": "nomor_spt", "label": "Nomor SPT"},
#         {"key": "judul", "label": "Judul"},
#         {"key": "created_at", "label": "Tanggal", "tipe": "date"},
#         {"key": "status", "label": "Status"},
#     ]
    
#     actions = [
#         {"key": "detail", "label": "Detail", "url": "core_spt_detail", "param": "spt_id"},
#         {"key": "upload", "label": "Upload Laporan", "url": "core_upload_laporan", "param": "spt_id"},
#     ]
    

#     context = {
#         "page_obj": page_obj,
#         "columns": columns,
#         "actions": actions,
#         "current_url": "pegawai_spt_list_htmx",
#         # "detail_url": "core_spt_detail",
#         # "upload_url": "core_upload_laporan",
#         # "judul_halaman": "Daftar Permohonan SPT",
#     }
    
#     if init:
#         return render(request, "partials/spt-list.html", context)
    
#     return render(request, "partials/_tabel-spt.html", context)

@login_required
# @roles_required("pegawai")
def disposisi_list_htmx(request):
    init = request.GET.get("init", "")
    q = request.GET.get("q", "")
    tanggal = request.GET.get("tanggal", "")
    page_number = request.GET.get("page")
    
    qs = get_disposisi_for_user(request.user)
    
    if q:
        qs = qs.filter(Q(nomor_spt__icontains=q) | Q(judul__icontains=q))
    
    if tanggal:
        qs = qs.filter(created_at__date=tanggal)
    
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(page_number)
    
    columns = [
        # {"key": "nomor_spt", "label": "Nomor SPT"},
        # {"key": "judul", "label": "Judul"},
        {"key": "created_at", "label": "Tanggal", "tipe": "date"},
        {"key": "status", "label": "Status"},
    ]
    
    actions = [
        {"key": "detail", "label": "Detail", "url": "disposisi_detail", "param": "id"},
        # {"key": "upload", "label": "Upload Laporan", "url": "core_upload_laporan", "param": "spt_id"},
    ]
    

    context = {
        "page_obj": page_obj,
        "columns": columns,
        "actions": actions,
    }
    
    if init:
        return render(request, "partials/disposisi-list.html", context)
    
    return render(request, "partials/_tabel.html", context)

# permohonan spt list htmx
@login_required
@roles_required("pegawai")
def permohonan_spt_list_htmx(request):
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
    
    spt_list = get_spt_list(request.user).order_by("-created_at")
    
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
    
    actions = [
        {"key": "detail", "label": "Detail", "url": "core_permohonan_spt_detail", "param": "id"},
        {"key": "upload", "label": "Upload Laporan", "url": "core_upload_laporan", "param": "id"},
        {"key": "delete", "label": "Hapus", "url": "core_permohonan_spt_delete", "param": "id"},
    ]
    

    context = {
        "page_obj": page_obj,
        "columns": columns,
        "actions": actions,
        "current_url": "pegawai_spt_list_htmx",
        # "detail_url": "core_spt_detail",
        # "upload_url": "core_upload_laporan",
        "judul_halaman": "Daftar Permohonan SPT",
    }
    
    if init:
        return render(request, "partials/permohonan-spt-list.html", context)
    
    return render(request, "partials/_tabel.html", context)


@login_required
@roles_required("pegawai")
def spt_list_diterima_htmx(request):
    init = request.GET.get("init", "")
    q = request.GET.get("q", "")
    tanggal = request.GET.get("tanggal", "")
    page_number = request.GET.get("page")
    
    today = timezone.now().date()
    
    spt_list = (
        get_spt()
        .filter(
            Q(status="selesai") | Q(status="disetujui_final") |
            Q(status=SPTStatus.DISETUJUI)
        )
    ) # hanya permohonan
    
    for obj in spt_list:
        obj.periode = f"{obj.tanggal_mulai:%d-%m-%Y} - {obj.tanggal_selesai:%d-%m-%Y}"
        
        obj.is_expired = obj.tanggal_selesai and obj.tanggal_selesai < today

        obj.has_laporan = obj.tugas.exists()
        
        obj.upload_laporan_url = "core_upload_laporan" if (obj.is_expired and not obj.has_laporan) else ""
    
    if q:
        spt_list = spt_list.filter(Q(nomor_spt__icontains=q) | Q(judul__icontains=q))
    
    if tanggal:
        spt_list = spt_list.filter(created_at__date=tanggal)
    
    paginator = Paginator(spt_list, 10)
    page_obj = paginator.get_page(page_number)
    
    columns = [
        {"key": "nomor_spt", "label": "No. SPT"},
        {"key": "judul", "label": "Judul"},
        {"key": "periode", "label": "Tanggal"},
        {"key": "upload_laporan_url", "label": "Laporan", "tipe": "url", "label_url": "Buat Laporan"},
        # {"key": "status", "label": "Status"},
    ]
    
    actions = [
        {"key": "detail", "label": "Detail", "url": "core_spt_detail", "param": "spt_id"},
        # {"key": "upload", "label": "Upload Laporan", "url": "core_upload_laporan", "param": "spt_id"},
    ]
    
    context = {
        "page_obj": page_obj,
        "columns": columns,
        "actions": actions,
        "current_url": "pegawai_spt_list_diterima_htmx",
    }
    
    if init:
        return render(request, "partials/spt-list.html", context)
    
    return render(request, "partials/_tabel-spt.html", context)
    
    

# @login_required
# @roles_required("pegawai")
# def spt_cari_list_htmx(request):
#     q = request.GET.get("q", "")
#     tanggal = request.GET.get("tanggal", "")
#     page_number = request.GET.get("page", 1)
    
#     spt_list = get_spt_list(request.user).order_by("-created_at")
    
#     if q:
#         spt_list = spt_list.filter(nomor_spt__icontains=q)
    
#     if tanggal:
#         spt_list = spt_list.filter(created_at__date=tanggal)
        
#     paginator = Paginator(spt_list, 10)
#     page_obj = paginator.get_page(page_number)
    
    
#     # spt_list = get_spt_list(request.user).order_by("-created_at").filter(nomor_spt__icontains=q)
#     context = {
#         "page_obj": page_obj,
#         "detail_url": "core_spt_detail",
#         "upload_url": "core_upload_laporan",
#     }
#     return render(request, "partials/_tabel-spt.html", context)


# -------------------------------------------pegawai--------------------------------
@login_required
@roles_required("pegawai")
def permohonan_spt(request):
    return render(request, "pages/pegawai/permohonan-spt.html")

@login_required
@roles_required("pegawai")
def pegawai(request):
    # spt_list = [
    #     {"id": 1, "judul": "SPT 1", "status": "diajukan"},
    #     {"id": 2, "judul": "SPT 2", "status": "diajukan"},
    # ]

    spt_list = SPT.objects.all()

    spt_form = SPTForm()

    context = {
        "total_spt": 10,
        "diajukan": 5,
        "selesai": 5,
        "spt_list": spt_list,
        "spt_form": spt_form,
    }
    return render(request, "pages/pegawai/dashboard-pegawai.html", context)

@login_required
@roles_required("pegawai")
def spt_saya(request):
    spt_list = get_spt_list(request.user).order_by("-created_at")
    context = {"spt_list": spt_list}
    return render(request, "pages/pegawai/spt-saya.html", context)

@login_required
@roles_required("pegawai")
def spt_diterima(request):
    spt_list = get_spt_diterima_list(request.user).order_by("-created_at")
    
    today = timezone.now().date()

    for spt in spt_list:
        spt.is_expired = spt.tanggal_selesai and spt.tanggal_selesai < today

        spt.has_laporan = spt.tugas.exists()
        
    print(spt_list)
    context = {"spt_list": spt_list}
    return render(request, "pages/pegawai/spt-diterima.html", context)

@login_required
@roles_required("pegawai")
def ajukan_spt(request):
    # print("ini ajukan spt")

    if request.method == "POST":
        lampiran = request.FILES.getlist("lampiran")
        data = request.POST.copy()

        spt = buat_spt(request.user, data=data, lampiran=lampiran)
        
        # tambahan
        # spt = update_by_action(spt, "buat_permohonan_spt")
        
        return redirect("core_spt_detail", spt_id=spt.id)
    return render(request, "pages/pegawai/ajukan-spt.html")

# kirim permohonan spt
@login_required
@roles_required("pegawai")
def kirim_pengajuan(request, spt_id):
    # spt = submit_spt(spt_id, request.user)
    spt = get_spt_detail(spt_id, request.user)
    
    # kirim permohonan (tambahan)
    ke_user = User.objects.filter(groups__name="kasubag").first()
    spt = update_by_action(
        spt, action="kirim_permohonan_spt",
        dari_user=request.user, ke_user=ke_user
    )
    
    return redirect("permohonan_list")
    # return render(request, 'pages/pegawai/kirim-pengajuan.html', {"spt": spt})

# @login_required
# @roles_required("pegawai")
# def spt_detail(request, spt_id):
#     spt = get_spt_detail(spt_id, request.user)
#     lampiran_list = spt.lampiran.all()
#     context = {"spt": spt, "lampiran_list": lampiran_list}

#     return render(request, "pages/pegawai/spt-detail.html", context)

@login_required
@roles_required("pegawai")
def permohonan_spt_detail(request, id):
    spt = get_spt_detail(id, request.user)
    lampiran_list = spt.lampiran.all()
    context = {"spt": spt, "lampiran_list": lampiran_list}

    return render(request, "pages/pegawai/permohonan-spt-detail.html", context)

@login_required
@roles_required("pegawai")
def permohonan_spt_delete(request, id):
    spt = get_spt_detail(id, request.user)
    spt.delete()
    return redirect("permohonan_list")

@login_required
@roles_required("pegawai")
def edit_revisi(request, spt_id):
    spt = get_spt_detail(spt_id, request.user)
    spt.status = SPTStatus.DRAFT
    spt.save()

    return redirect("core_spt_revisi", spt_id=spt_id)

@login_required
@roles_required("pegawai")
def spt_revisi(request, spt_id):
    spt = get_spt_detail(spt_id, request.user)
    lampiran_list = get_lampiran_spt_list(spt_id)
    if request.method == "POST":
        # data = request.POST.copy()
        # data['status'] = SPTStatus.DRAFT
        # data['nomor_spt'] = ""
        spt_form = SPTFormRevisi(instance=spt, data=request.POST)
        if spt_form.is_valid():
            data = spt_form.cleaned_data
            spt = update_draft_spt(spt, request.user, data=data)

            # print("berhasil update")
            return redirect("core_spt_detail", spt_id=spt.id)
        else:
            # print("ini jalan")
            # print(spt_form.errors)
            context = {"form": spt_form, "spt": spt}
            render(request, "pages/pegawai/spt-revisi.html", context)

    context = {
        "spt": spt,
        "lampiran_list": lampiran_list,
        "spt_form": SPTForm(instance=spt),
    }
    return render(request, "pages/pegawai/spt-revisi.html", context)

@login_required
@roles_required("pegawai")
def upload_laporan_oleh_pegawai(request, spt_id):
    spt = get_spt_detail(spt_id, request.user)

    if request.method == "POST":
        tugas_pelaksanaan_form = TugasPelaksanaanForm(request.POST, request.FILES)
        if tugas_pelaksanaan_form.is_valid():
            data_form = tugas_pelaksanaan_form.cleaned_data
            tugas_pelaksanaan = upload_laporan_service(request, spt_id, data_form)
            # tugas_pelaksanaan = tugas_pelaksanaan_form.save(commit=False)

            # # inject field backend
            # tugas_pelaksanaan.spt = SPT.objects.get(id=spt_id)
            # tugas_pelaksanaan.pegawai = request.user
            # tugas_pelaksanaan.laporan = ""
            # tugas_pelaksanaan.status = "proses"

            # tugas_pelaksanaan.save()

            return redirect("core_spt_diterima")
    else:
        tugas_pelaksanaan_form = TugasPelaksanaanForm()

    context = {"tugas_pelaksanaan_form": tugas_pelaksanaan_form, "spt": spt}
    return render(request, "pages/pegawai/upload-laporan.html", context)