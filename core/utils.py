from spt.models import SPTStatus, SPT, PermohonanSPT
from workflow.models import Disposisi
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User

# STATE_MACHINE = {
#     "draft": {
#         "submit": "submitted",
#     },
#     "submitted": {
#         "approve": "approved",
#         "reject": "rejected",
#     },
#     "approved": {},
#     "rejected": {},
# }

# STATE_MACHINE = {
#     SPTStatus.DRAFT: {
#         "submit": SPTStatus.SUBMITTED,
#     },
#     SPTStatus.SUBMITTED: {
#         "approve": SPTStatus.APPROVED,
#         "reject": SPTStatus.REJECTED,
#     },
#     SPTStatus.APPROVED: {},
#     SPTStatus.REJECTED: {},
# }

# [DRAFT] --submit--> [SUBMITTED]
# [SUBMITTED] --approve--> [APPROVED]
# [SUBMITTED] --reject--> [REJECTED]

class InvalidAction(Exception):
    pass


# def update_status_by_action(obj, action: str, machine: dict, save=True):
#     current = obj.status

#     state_actions = machine.get(current, {})

#     if action not in state_actions:
#         raise InvalidAction(
#             f"Aksi '{action}' tidak valid dari status '{current}'"
#         )

#     new_status = state_actions[action]

#     obj.status = new_status

#     if save:
#         obj.save(update_fields=["status"])

#     return obj

# cara penggunaan:
# update_status_by_action(obj, "approve", STATE_MACHINE)

# di template
# def get_available_actions(obj, machine: dict):
#     return list(machine.get(obj.status, {}).keys())



# -------- jika menggunakan handler



# kumpulan handler
def buat_permohonan_spt_action(obj):        
    return obj
    
    

def submit_action(obj):
    obj.status = SPTStatus.SUBMITTED
    obj.submitted_at = timezone.now()
    # obj.save(update_fields=["status", "submitted_at"])

# handler2
def approve_action(obj):
    obj.status = SPTStatus.APPROVED
    # obj.approved_at = timezone.now()
    # obj.save(update_fields=["status", "approved_at"]) # baiknya jangan save disini tapi di controler

# STATE_MACHINE = {
#     SPTStatus.DRAFT: {
#         "buat_permohonan_spt": buat_permohonan_spt_action,
#     },
#     SPTStatus.SUBMITTED: {
#         "approve": approve_action,
#     },
# }

def kirim_permohonan_spt_action(spt, dari_user, ke_user):
    Disposisi.objects.create(
        spt=spt,
        dari_user=dari_user,
        ke_user=ke_user,
        status=SPTStatus.DIAJUKAN
    )

STATE_MACHINE = {
    SPTStatus.DRAFT: {
        "kirim_permohonan_spt": {
            # "handler": buat_permohonan_spt_action, # bisa None
            "handler": kirim_permohonan_spt_action, # bisa None
            "next_state_spt": SPTStatus.PERMOHONAN_DIAJUKAN,
            "next_state_permohonan": SPTStatus.PERMOHONAN_DIAJUKAN
        },
    },
    SPTStatus.REVIEW_KASUBAG: {
        "setujui_permohonan_oleh_kasubag": {
            "handler": None,
            "next_state_spt": SPTStatus.KASUBAG_SETUJUI_PERMOHOAN,
            "next_state_permohonan": SPTStatus.KASUBAG_SETUJUI_PERMOHOAN
        },
        "tolak_permohonan_oleh_kasubag": {
            "handler": None,
            "next_state_spt": SPTStatus.DITOLAK_KASUBAG,
            "next_state_permohonan": SPTStatus.DITOLAK_KASUBAG
        },
    },
    # SPTStatus.PERMOHONAN_DISETUJUI_PIMPINAN: {
    #     "setujui_permohonan_oleh_pimpinan": {
    #         "handler": None,
    #         "next_state_spt": None,
    #         "next_state_permohonan": SPTStatus.PERMOHONAN_DISETUJUI_PIMPINAN
    #     },
    #     "tolak_permohonan_oleh_pimpinan": {
    #         "handler": None,
    #         "next_state_spt": SPTStatus.DITOLAK_PIMPINAN,
    #         "next_state_permohonan": SPTStatus.DITOLAK_PIMPINAN
    #     },
    # }
    # SPTStatus.PERMOHONAN_DIAJUKAN: {
    #     "review_permohonan_oleh_kasubag": {
    #         "handler": None,
    #         "next_state_spt": SPTStatus.REVIEW_KASUBAG,
    #         "next_state_permohonan": SPTStatus.REVIEW_KASUBAG
    #     },
    # },
}

# fungsi eksekutor
def update_by_action(obj: SPT, action: str, machine: dict=STATE_MACHINE, **kwargs):
    current = obj.status
    
    config = machine.get(current, {}).get(action)
    if not config:
        raise Exception("Invalid action")
    
    handler = config['handler']
    if handler:
        handler(obj, **kwargs) # jalankan kalau ada
    
    # update state di satu tempat
    with transaction.atomic():
        # update status spt
        if config["next_state_spt"]:
            obj.status = config["next_state_spt"]
            obj.save()
        
        # update status pemohonan
        if config["next_state_permohonan"]:
            permohohonan_spt = obj.permohonan_spt
            permohohonan_spt.status = config["next_state_permohonan"]
            permohohonan_spt.save()
        
    return obj

    # actions = machine.get(current)
    # if not actions:
    #     raise Exception(f"State '{current}' tidak terdaftar")

    # handler = actions.get(action)
    # if not handler:
    #     raise Exception(f"Aksi '{action}' tidak valid untuk state '{current}'")

    # return handler(obj)

# cara pakai
# update_by_action(obj, "submit", STATE_MACHINE)

# def update_by_action(obj, action, machine):
#     config = machine[obj.status][action]

#     obj.status = config["next"]

#     if "handler" in config:
#         config["handler"](obj)  # panggil handler

#     obj.save()

#     return obj

from datetime import datetime, date

HARI_INDONESIA = {
    0: "Senin",
    1: "Selasa",
    2: "Rabu",
    3: "Kamis",
    4: "Jumat",
    5: "Sabtu",
    6: "Minggu",
}

BULAN_INDONESIA = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember",
}


def format_tanggal_indonesia(tanggal_str: str) -> str:
    """
    Mengubah:
        '20-01-2026'

    Menjadi:
        'Selasa, 20 Januari 2026'
    """

    tanggal = datetime.strptime(tanggal_str, "%d-%m-%Y")

    hari = HARI_INDONESIA[tanggal.weekday()]
    tanggal_angka = tanggal.day
    bulan = BULAN_INDONESIA[tanggal.month]
    tahun = tanggal.year

    return f"{hari}, {tanggal_angka} {bulan} {tahun}"

def format_date_indonesia(tanggal: date) -> str:
    hari = HARI_INDONESIA[tanggal.weekday()]
    bulan = BULAN_INDONESIA[tanggal.month]

    return f"{hari}, {tanggal.day} {bulan} {tanggal.year}"


# core/utils/date.py

from django.utils import timezone

MONTHS_ID = {
    1: "Januari",
    2: "Februari",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Agustus",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Desember",
}


def format_tanggal_indonesia_django(date):
    return (
        f"{date.day} "
        f"{MONTHS_ID[date.month]} "
        f"{date.year}"
    )