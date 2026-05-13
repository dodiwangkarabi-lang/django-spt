from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import reverse
from spt.forms import SPTForm, SPTFormRevisi
from spt.models import SPT, SPTLampiran, SPTStatus
from spt.services_old import (
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

# -------------------------------------------guest--------------------------------
def register(request):
    return render(request, "pages/guests/register.html")


def login_view(request):
    return render(request, "pages/guests/login.html")