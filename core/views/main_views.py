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