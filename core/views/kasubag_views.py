from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse
from spt.forms import SPTForm, SPTFormRevisi
from spt.models import SPT, SPTLampiran, SPTStatus
from spt.services import (
    create_spt,
    get_spt_list,
    get_spt_detail,
    get_inbox_disposisi,
    get_disposisi_detail,
    kasubbag_approve,
    kasubbag_reject,
    kasubbag_revisi,
    kasubbag_terima_spt,
    kasubbag_review,
    update_draft_spt_kasubag,
    pimpinan_approve,
    pimpinan_reject,
    pimpinan_revisi,
    update_draft_spt,
    simpan_draft_spt,
    submit_spt,
    upload_lampiran_spt,
    delete_lampiran_spt,
    get_lampiran_spt_detail,
    get_lampiran_spt_list,
    buat_spt,
    get_spt_diterima_list,
    get_kasubag_user,
    get_pimpinan_user,
    pimpinan_setujui_permohonan,
    update_dan_create_disposisi_baru,
)

# timezone
from django.utils import timezone

from accounts.models import Profile
from accounts.forms import UserUpdateForm

from tugas.forms import TugasPelaksanaanForm
from tugas.models import TugasPelaksanaan
from tugas.services import upload_laporan_service, is_laporan_exist

from core.decorators import roles_required

from spt.analisis_services import RangkumanSPT

# -------------------------------------------kasugab--------------------------------
@login_required
@roles_required("kasubag")
def buat_spt_kasubag_view(request, disposisi_id):
    disposisi = get_disposisi_detail(disposisi_id, request.user)
    spt = disposisi.spt
    lampiran_list = get_lampiran_spt_list(spt.id)
    if request.method == "POST":
        # data = request.POST.copy()
        # data['status'] = SPTStatus.DRAFT
        # data['nomor_spt'] = ""
        spt_form = SPTFormRevisi(instance=spt, data=request.POST)
        if spt_form.is_valid():
            data = spt_form.cleaned_data

            spt = update_draft_spt_kasubag(spt, request.user, data=data)
            pimpinan = get_pimpinan_user()

            catatan = "Pengajuan SPT oleh kasubag"
            status_spt = SPTStatus.REVIEW_SPT_PIMPINAN
            disposisi_baru = update_dan_create_disposisi_baru(
                disposisi,
                spt=spt,
                pengirim=request.user,
                penerima=pimpinan,
                catatan=catatan,
                status=status_spt,
            )

            # print("berhasil update")
            return redirect("core_kasubag_disposisi")
        else:
            # print("ini jalan")
            print(spt_form.errors)
            context = {"form": spt_form, "spt": spt}
            render(request, "pages/kasubag/spt-revisi.html", context)

    context = {
        "spt": spt,
        "lampiran_list": lampiran_list,
        "spt_form": SPTForm(instance=spt),
    }
    return render(request, "pages/kasubag/spt-revisi.html", context)

@login_required
@roles_required("kasubag")
def review_permohonan(request, disposisi_id):
    disposisi = get_disposisi_detail(disposisi_id, request.user)

    kasubbag_review(disposisi, request.user)

    return redirect("core_kasubag_disposisi_detail", disposisi_id=disposisi_id)

@login_required
@roles_required("kasubag")
def daftar_spt_diajukan(request):
    spt_list = get_spt_list()
    context = {"spt_list": spt_list}
    return render(request, "pages/kasubag/daftar-spt-diajukan.html", context)

@login_required
@roles_required("kasubag")
def kasubag(request):
    rangkuman_spt = RangkumanSPT()
    context = {
        "total_spt": rangkuman_spt.total_spt(),
        "sedang_direview": rangkuman_spt.total_proses_review_kasubag(),
        "belum_direview": rangkuman_spt.total_permohonan_belum_direview(),
    }
    return render(request, "pages/kasubag/dashboard-kasubag.html", context)

@login_required
@roles_required("kasubag")
def review_spt(request, spt_id):
    spt = SPT.objects.get(id=spt_id)
    context = {"spt": spt}
    return render(request, "pages/kasubag/review-spt.html", context)

@login_required
@roles_required("kasubag")
def disposisi(request):
    disposisi_list = get_inbox_disposisi(request.user)
    context = {"disposisi_list": disposisi_list}
    return render(request, "pages/kasubag/disposisi.html", context)

@login_required
@roles_required("kasubag")
def disposisi_detail(request, disposisi_id):
    disposisi = get_disposisi_detail(disposisi_id, request.user)
    context = {"disposisi": disposisi}
    return render(request, "pages/kasubag/disposisi-detail.html", context)

@login_required
@roles_required("kasubag")
def approve(request, disposisi_id):
    if request.method == "POST":
        pimpinan_user = User.objects.filter(groups__name="pimpinan").first()
        disposisi = get_disposisi_detail(disposisi_id, request.user)
        disposisi = kasubbag_approve(
            disposisi, kasubbag_user=request.user, pimpinan_user=pimpinan_user
        )
        return redirect("core_kasubag_disposisi")
    else:
        context = {"disposisi": disposisi}
        return render(request, "pages/kasubag/approval.html", context)

@login_required
@roles_required("kasubag")
def reject(request, disposisi_id):
    if request.method == "POST":
        catatan = request.POST["catatan"]
        disposisi = get_disposisi_detail(disposisi_id, request.user)

        spt = kasubbag_reject(disposisi, request.user, catatan=catatan)
        return redirect("core_kasubag_disposisi")

    else:
        return render(request, "pages/kasubag/reject.html")

@login_required
@roles_required("kasubag")
def revisi(request, disposisi_id):
    if request.method == "POST":
        pegawai_id = request.POST["pegawai_id"]
        catatan = request.POST["catatan"]
        disposisi = get_disposisi_detail(disposisi_id, request.user)
        pegawai_user = User.objects.get(id=pegawai_id)

        kasubbag_revisi(disposisi, request.user, penerima_user=pegawai_user, catatan=catatan)
        return redirect("core_kasubag_disposisi")

    return render(request, "pages/kasubag/revisi.html")

@login_required
@roles_required("kasubag")
def approval_spt(request):
    return render(request, "pages/kasubag/approval-spt.html")
