from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone

from .models import SPT, SPTLampiran, SPTStatus
from workflow.models import Disposisi, DisposisiTemplate, DisposisiTipe

from spt.utils import generate_nomor_spt

from .pdf_service import generate_spt_pdf
# -----------------------------------------------

# ----------------------dokumen-------------------------
@transaction.atomic
def approve_final_spt(spt_id, pimpinan_id):
    spt = get_object_or_404(SPT, id=spt_id)
    pimpinan = get_object_or_404(User, id=pimpinan_id)
    
    if spt.status != SPTStatus.DIAJUKAN:
        raise Exception("SPT tidak bisa di-approve")

    spt.status = SPTStatus.DISETUJUI
    spt.disetujui_oleh = pimpinan
    spt.tanggal_ttd = timezone.now()

    # generate PDF
    pdf_file = generate_spt_pdf(spt)

    spt.file_final.save(f"spt_{spt.id}.pdf", pdf_file)
    spt.save()

    return spt


# ------------------main-----------------------------

def get_kasubag_user():
    return User.objects.filter(groups__name="kasubag").first()

def get_pimpinan_user():
    return User.objects.filter(groups__name="pimpinan").first()

@transaction.atomic
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

@transaction.atomic
def delete_lampiran_spt(lampiran_id):
    lampiran = get_object_or_404(SPTLampiran, id=lampiran_id)
    lampiran.delete()
    return lampiran

@transaction.atomic
def get_lampiran_spt_list(spt_id):
    spt = get_object_or_404(SPT, id=spt_id)
    lampiran = spt.lampiran.all()
    return lampiran

def get_lampiran_spt_detail(lampiran_id):
    lampiran = get_object_or_404(SPTLampiran, id=lampiran_id)
    return lampiran

@transaction.atomic
def update_draft_spt_kasubag(spt: SPT, user, data):
    """
    Update SPT jika sebagai kasubag
    """
    
    # validasi kasubag
    if get_kasubag_user() != user:
        raise ValueError("anda bukan kasubag")

    # validasi ownership
    # if spt.dibuat_oleh != user:
    #     raise ValueError("Tidak boleh mengubah SPT ini")

    # hanya draft yang boleh diubah
    # if spt.status != SPTStatus.DRAFT:
    #     raise ValueError("Hanya SPT draft yang bisa diubah")

    # update field (aman + fallback)
    spt.nomor_spt = data.get("nomor_spt", spt.nomor_spt)
    spt.judul = data.get("judul", spt.judul)
    spt.deskripsi = data.get("deskripsi", spt.deskripsi)
    spt.tanggal_mulai = data.get("tanggal_mulai", spt.tanggal_mulai)
    spt.tanggal_selesai = data.get("tanggal_selesai", spt.tanggal_selesai)
    # spt.status = data.get("status", spt.status)
    spt.status = SPTStatus.KASUBAG_AJUKAN_SPT

    spt.save()

    return spt

def update_dan_create_disposisi_baru(disposisi: Disposisi, spt: SPT, pengirim: User, penerima: User, catatan="", status=None):
    """keterangan

    Args:
        disposisi (Disposisi): Disposisi lama
        

    Returns:
        Disposisi: Disposisi baru
    """
    # spt = disposisi.spt
    # update disposisi lama
    disposisi.status = SPTStatus.DISETUJUI
    disposisi.save()

    # update status SPT
    spt.status = status
    spt.save()

    # create disposisi ke pimpinan
    return Disposisi.objects.create(
        spt=spt,
        dari_user=pengirim,
        ke_user=penerima,
        status=SPTStatus.DIAJUKAN,
        catatan=catatan or "Diteruskan ke pimpinan"
    )


@transaction.atomic
def update_draft_spt(spt: SPT, user, data):
    """
    Update SPT hanya jika masih draft
    """

    # validasi ownership
    if spt.dibuat_oleh != user:
        raise ValueError("Tidak boleh mengubah SPT ini")

    # hanya draft yang boleh diubah
    if spt.status != SPTStatus.DRAFT:
        raise ValueError("Hanya SPT draft yang bisa diubah")

    # update field (aman + fallback)
    spt.nomor_spt = data.get("nomor_spt", spt.nomor_spt)
    spt.judul = data.get("judul", spt.judul)
    spt.deskripsi = data.get("deskripsi", spt.deskripsi)
    spt.tanggal_mulai = data.get("tanggal_mulai", spt.tanggal_mulai)
    spt.tanggal_selesai = data.get("tanggal_selesai", spt.tanggal_selesai)
    # spt.status = data.get("status", spt.status)
    spt.status = SPTStatus.DRAFT

    spt.save()

    return spt

@transaction.atomic
def simpan_draft_spt(user, data):
    """
    Simpan SPT sebagai draft (belum diajukan)
    """

    spt = SPT.objects.create(
        created_by=user,
        nomor_spt=data.get("nomor_spt"),
        judul=data.get("judul"),
        deskripsi=data.get("deskripsi"),
        tanggal=data.get("tanggal"),

        # status awal
        status="draft"
    )

    return spt


def approve_spt(spt_id, user):
    spt = get_object_or_404(SPT, id=spt_id)

    # validasi role
    if not user.groups.filter(name="kasubbag").exists():
        raise Exception("Tidak punya akses")

    spt.status = SPTStatus.DISETUJUI
    spt.save()

    return spt

    # def approve_spt(spt_id, user):
    #     spt = SPT.objects.get(id=spt_id)

    #     if not user.groups.filter(name="pimpinan").exists():
    #         raise Exception("Tidak punya akses")

    #     if spt.status != "diajukan":
    #         raise Exception("SPT belum diajukan")

    #     spt.status = "disetujui"
    #     spt.save()

    return spt


# def create_spt(user, data):
#     spt = SPT.objects.create(
#         tujuan=data.get("tujuan"),
#         tanggal=data.get("tanggal"),
#         created_by=user,
#         status="draft"
#     )
#     return spt

@transaction.atomic
def buat_spt(user, data, lampiran=None):
    """penjelasan

    Args:
        data: queryset -> fields:["nomor_spt", "judul", "deskripsi", "tanggal_mulai", "tanggal_selesai", "lampiran"]

    Returns:
        spt: instance object dari SPT
    """
    # buat spt
    spt = SPT.objects.create(
        nomor_spt=data.get("nomor_spt"),
        judul=data.get("judul"),
        deskripsi=data.get("deskripsi"),
        tanggal_mulai=data.get("tanggal_mulai"),
        tanggal_selesai=data.get("tanggal_selesai"),
        dibuat_oleh=user,
        status="draft",
    )
    if lampiran:
        for lamp in lampiran:
            data_lampiran = {
                "file": lamp,
                "keterangan": data.get("keterangan", ""),
            }
            upload_lampiran_spt(spt.id, data_lampiran)
    
    return spt
    
def create_spt(user, data):
    with transaction.atomic():
        # buat spt
        spt = SPT.objects.create(
            nomor_spt=data.get("nomor_spt"),
            judul=data.get("judul"),
            deskripsi=data.get("deskripsi"),
            tanggal_mulai=data.get("tanggal_mulai"),
            tanggal_selesai=data.get("tanggal_selesai"),
            dibuat_oleh=user,
            status="draft",
        )

        # kasubag tujuan
        kasubag = User.objects.filter(groups__name="kasubag").first()
        if not kasubag:
            raise Exception("Kasubag tidak ditemukan")

        Disposisi.objects.create(
            spt=spt, dari_user=user, ke_user=kasubag, status="diajukan"
        )

        return spt


def update_spt(spt_id, user, data):
    spt = SPT.objects.get(id=spt_id)

    if spt.dibuat_oleh != user:
        raise Exception("Bukan pemilik SPT")

    if spt.status not in ["draft", "direvisi"]:
        raise Exception("SPT tidak bisa diedit")

    spt.nomor_spt = data.get("nomor_spt")
    spt.judul = data.get("judul")
    spt.deskripsi = data.get("deskripsi")
    spt.tanggal_mulai = data.get("tanggal_mulai")
    spt.tanggal_selesai = data.get("tanggal_selesai")

    spt.save()
    return spt


# def update_spt(spt_id, data):
#     spt = SPT.objects.get(id=spt_id)

#     spt.tujuan = data.get("tujuan")
#     spt.tanggal = data.get("tanggal")
#     spt.status = "revisi"

#     spt.save()
#     return spt

# def submit_spt(spt_id):
#     spt = SPT.objects.get(id=spt_id)
#     spt.status = "diajukan"
#     spt.save()
#     return spt


@transaction.atomic
def submit_spt(spt_id, user):
    spt = SPT.objects.get(id=spt_id)

    if spt.dibuat_oleh != user:
        raise Exception("Bukan pemilik SPT")

    if spt.status != "draft":
        raise Exception("Hanya draft yang bisa diajukan")

    spt.status = SPTStatus.PERMOHONAN_DIAJUKAN
    spt.save()
    
    Disposisi.objects.create(
        spt=spt,
        dari_user=user,
        ke_user=User.objects.filter(groups__name="kasubag").first(),
        status="diajukan"
    )

    return spt


# def delete_spt(spt_id):
#     spt = SPT.objects.get(id=spt_id)
#     spt.delete()


def delete_spt(spt_id, user):
    spt = SPT.objects.get(id=spt_id)

    if spt.dibuat_oleh != user:
        raise Exception("Bukan pemilik")

    if spt.status != "draft":
        raise Exception("Hanya draft yang bisa dihapus")

    spt.delete()


def review_spt(spt_id, user, action):
    spt = SPT.objects.get(id=spt_id)

    if not user.groups.filter(name="kasubbag").exists():
        raise Exception("Tidak punya akses")

    if action == "approve":
        spt.status = "disetujui_kasubbag"
    elif action == "revisi":
        spt.status = "perlu_revisi"
    elif action == "tolak":
        spt.status = "ditolak"

    spt.save()
    return spt


def approve_final(spt_id, user):
    spt = SPT.objects.get(id=spt_id)

    if not user.groups.filter(name="pimpinan").exists():
        raise Exception("Tidak punya akses")

    spt.status = SPTStatus.FINAL
    spt.save()

    return spt


def upload_laporan(spt_id, file, user):
    spt = SPT.objects.get(id=spt_id)

    spt.laporan = file
    spt.status = SPTStatus.SELESAI
    spt.save()

    return spt


# def get_spt_list(user):
#     if user.groups.filter(name="pegawai").exists():
#         return SPT.objects.filter(created_by=user)

#     if user.groups.filter(name="kasubbag").exists():
#         return SPT.objects.filter(status="diajukan")

#     if user.groups.filter(name="pimpinan").exists():
#         return SPT.objects.filter(status="disetujui_kasubbag")

#     return SPT.objects.none()


def get_spt_list(user):
    if user.groups.filter(name="pegawai").exists():
        return SPT.objects.filter(dibuat_oleh=user)

    if user.groups.filter(name="pimpinan").exists():
        return SPT.objects.filter(status="diajukan")

    return SPT.objects.none()

def get_spt_diterima_list(user):
    if user.groups.filter(name="pegawai").exists():
        return SPT.objects.filter(dibuat_oleh=user).filter(Q(status="disetujui_final") | Q(status="selesai"))

    if user.groups.filter(name="pimpinan").exists():
        return SPT.objects.filter(status=SPTStatus.DIAJUKAN)

    return SPT.objects.none()


# def get_kasubbag_spt_inbox():
#     return SPT.objects.filter(status="diajukan")


def get_inbox_disposisi(user):
    disposisi_list = Disposisi.objects.filter(ke_user=user, status="diajukan").order_by(
        "-created_at"
    )
    return disposisi_list

def get_disposisi_detail(disposisi_id, user):
    disposisi = Disposisi.objects.get(id=disposisi_id)

    if disposisi.ke_user != user:
        raise Exception("Bukan pemilik disposisi")

    return disposisi


def get_spt_detail(spt_id, user):
    spt = SPT.objects.get(id=spt_id)

    if spt.dibuat_oleh != user:
        raise Exception("Bukan pemilik SPT")

    return spt


def reject_spt(spt_id, user):
    spt = SPT.objects.get(id=spt_id)

    if not user.groups.filter(name="pimpinan").exists():
        raise Exception("Tidak punya akses")

    if spt.status != "diajukan":
        raise Exception("SPT belum diajukan")

    spt.status = "ditolak"
    spt.save()

    return spt


def revise_spt(spt_id, user):
    spt = SPT.objects.get(id=spt_id)

    if not user.groups.filter(name="pimpinan").exists():
        raise Exception("Tidak punya akses")

    if spt.status != "diajukan":
        raise Exception("SPT belum diajukan")

    spt.status = "direvisi"
    spt.save()

    return spt


@transaction.atomic
def kasubbag_terima_spt(disposisi: Disposisi, kasubbag_user):
    """
    Kasubbag menerima SPT dari pegawai melalui disposisi.
    Biasanya ini terjadi saat membuka / mulai memproses SPT.
    """

    # validasi: pastikan disposisi memang untuk kasubbag ini
    if disposisi.ke_user != kasubbag_user:
        raise ValueError("Tidak berhak mengakses disposisi ini")

    # validasi: hanya yang masih diajukan
    if disposisi.status != "diajukan":
        raise ValueError("Disposisi sudah diproses")

    spt = disposisi.spt

    # update status SPT → masuk tahap review kasubbag
    spt.status = SPTStatus.REVIEW_KASUBBAG
    spt.save()

    # OPTIONAL: bisa tandai disposisi sebagai "diproses"
    # kalau kamu ingin tracking lebih detail
    # disposisi.status = "diproses"
    # disposisi.save()

    return spt


@transaction.atomic
def pimpinan_terima_spt(
    disposisi: Disposisi, pimpinan_user, keputusan: str, catatan: str = ""
):
    """
    Service pimpinan untuk menerima/memproses SPT dari kasubbag.

    keputusan:
        - disetujui
        - ditolak
        - revisi
    """

    spt = disposisi.spt

    # validasi: pastikan disposisi memang untuk pimpinan ini
    if disposisi.ke_user != pimpinan_user:
        raise ValueError("Tidak berhak memproses disposisi ini")

    # update status disposisi lama (dari kasubbag)
    disposisi.status = keputusan
    disposisi.catatan = catatan
    disposisi.save()

    # update status SPT sesuai keputusan pimpinan
    if keputusan == "disetujui":
        spt.status = SPTStatus.DISETUJUI_FINAL

    elif keputusan == "ditolak":
        spt.status = SPTStatus.DITOLAK_PIMPINAN

    elif keputusan == "revisi":
        spt.status = SPTStatus.REVISI_PIMPINAN

    else:
        raise ValueError("Keputusan tidak valid")

    spt.save()

    return spt


# =========================================================
# review (Kasubbag review permohonan)
# =========================================================
@transaction.atomic
def kasubbag_review(disposisi: Disposisi, kasubbag_user):
    if disposisi.ke_user != kasubbag_user:
        raise ValueError("Tidak berhak memproses disposisi ini")
    
    spt = disposisi.spt
    spt.status = SPTStatus.REVIEW_KASUBAG
    spt.save()
    
    return disposisi



# =========================================================
# 1. APPROVE (Kasubbag → lanjut ke Pimpinan)
# =========================================================
@transaction.atomic
def kasubbag_approve(disposisi: Disposisi, kasubbag_user, pimpinan_user):
    """
    Kasubbag menyetujui SPT → lanjut ke pimpinan
    """

    if disposisi.ke_user != kasubbag_user:
        raise ValueError("Tidak berhak memproses disposisi ini")

    if disposisi.status != SPTStatus.DIAJUKAN:
        raise ValueError("Disposisi sudah diproses")

    spt = disposisi.spt

    # update disposisi lama
    disposisi.status = SPTStatus.DISETUJUI
    disposisi.save()

    # update status SPT
    spt.status = SPTStatus.REVIEW_PIMPINAN
    spt.save()

    # create disposisi ke pimpinan
    return Disposisi.objects.create(
        spt=spt,
        dari_user=kasubbag_user,
        ke_user=pimpinan_user,
        status=SPTStatus.DIAJUKAN,
        catatan="Diteruskan ke pimpinan"
    )
    
# =========================================================
# 2. REJECT (Kasubbag menolak SPT)
# =========================================================
@transaction.atomic
def kasubbag_reject(disposisi: Disposisi, kasubbag_user, catatan=""):
    """
    Kasubbag menolak SPT → proses selesai
    """

    if disposisi.ke_user != kasubbag_user:
        raise ValueError("Tidak berhak memproses disposisi ini")

    if disposisi.status != SPTStatus.DIAJUKAN:
        raise ValueError("Disposisi sudah diproses")

    spt = disposisi.spt

    # update disposisi
    disposisi.status = SPTStatus.DITOLAK
    # disposisi.catatan = catatan
    disposisi.save()

    # update SPT
    spt.status = SPTStatus.DITOLAK_KASUBAG
    spt.catatan = catatan
    spt.save()

    return spt

# =========================================================
# 3. REVISI (Kasubbag minta perbaikan ke pegawai)
# =========================================================
@transaction.atomic
def kasubbag_revisi(disposisi: Disposisi, kasubbag_user, penerima_user, catatan=""):
    """
    Kasubbag mengembalikan SPT ke pegawai untuk direvisi
    """

    if disposisi.ke_user != kasubbag_user:
        raise ValueError("Tidak berhak memproses disposisi ini")

    if disposisi.status != SPTStatus.DIAJUKAN:
        raise ValueError("Disposisi sudah diproses")

    spt = disposisi.spt

    # update disposisi lama
    disposisi.status = SPTStatus.REVISI
    # disposisi.catatan = catatan
    disposisi.save()

    # update SPT
    spt.status = SPTStatus.REVISI_KASUBAG
    spt.catatan = catatan
    spt.save()

    # create disposisi balik ke pegawai
    return Disposisi.objects.create(
        spt=spt,
        dari_user=kasubbag_user,
        ke_user=penerima_user,
        status=SPTStatus.DIAJUKAN,
        catatan=catatan
    )
    
# =========================================================
# *. Setujui Permohonan (Pimpinan menyetujui)
# =========================================================
@transaction.atomic
def pimpinan_setujui_permohonan(disposisi: Disposisi, pimpinan_user, kasubag_user="", catatan=""):
    """
    Pimpinan menyetujui permohonan SPT
    """

    if disposisi.ke_user != pimpinan_user:
        raise ValueError("Tidak berhak memproses disposisi ini")

    if disposisi.status != SPTStatus.DIAJUKAN:
        raise ValueError("Sudah diproses")

    

    # update disposisi
    disposisi.status = SPTStatus.DISETUJUI
    disposisi.save()

    # update SPT
    spt = disposisi.spt
    spt.status = SPTStatus.PERMOHONAN_DISETUJUI_PIMPINAN
    spt.save()
    
    # create disposisi balik ke pegawai
    if not kasubag_user:
        kasubag_user = get_kasubag_user()
    return Disposisi.objects.create(
        spt=spt,
        dari_user=pimpinan_user,
        ke_user=kasubag_user,
        status=SPTStatus.DIAJUKAN,
        catatan=catatan
    )

    



# =========================================================
# 1. APPROVE FINAL (Pimpinan menyetujui)
# =========================================================
@transaction.atomic
def pimpinan_approve(disposisi: Disposisi, pimpinan_user):
    """
    Pimpinan menyetujui SPT → final approved
    """

    if disposisi.ke_user != pimpinan_user:
        raise ValueError("Tidak berhak memproses disposisi ini")

    if disposisi.status != SPTStatus.DIAJUKAN:
        raise ValueError("Sudah diproses")

    spt = disposisi.spt

    # update disposisi
    disposisi.status = SPTStatus.DISETUJUI
    disposisi.save()

    # update SPT FINAL
    spt.status = SPTStatus.DISETUJUI_FINAL
    spt.nomor_spt = generate_nomor_spt()
    spt.save()

    return spt


# =========================================================
# 2. REJECT (Pimpinan menolak)
# =========================================================
@transaction.atomic
def pimpinan_reject(disposisi: Disposisi, pimpinan_user, catatan=""):
    """
    Pimpinan menolak SPT → selesai
    """

    if disposisi.ke_user != pimpinan_user:
        raise ValueError("Tidak berhak memproses disposisi ini")

    if disposisi.status != SPTStatus.DIAJUKAN:
        raise ValueError("Sudah diproses")

    spt = disposisi.spt

    disposisi.status = SPTStatus.DITOLAK
    # disposisi.catatan = catatan
    disposisi.save()

    spt.status = SPTStatus.DITOLAK_PIMPINAN
    spt.catatan = catatan
    spt.save()

    return spt

@transaction.atomic
def pimpinan_revisi(disposisi: Disposisi, pimpinan_user, penerima, catatan=""):
    """
    Pimpinan mengembalikan SPT ke penerima untuk direvisi
    """

    if disposisi.ke_user != pimpinan_user:
        raise ValueError("Tidak berhak memproses disposisi ini")

    if disposisi.status != SPTStatus.DIAJUKAN:
        raise ValueError("Disposisi sudah diproses")

    spt = disposisi.spt

    # update disposisi lama
    disposisi.status = SPTStatus.REVISI
    
    # jika catatan tidak di isi, maka gunakan catatan dari template
    template = DisposisiTemplate.objects.get(tipe=DisposisiTipe.REVISI)
    if not catatan:
        if template:
            catatan = template.teks_default
        else:
            catatan = " " # fallback ke string kosong
    
    disposisi.catatan = catatan
    disposisi.save()

    # update SPT
    spt.status = SPTStatus.REVISI_PIMPINAN
    spt.catatan = catatan
    spt.save()

    # create disposisi balik ke pegawai
    return Disposisi.objects.create(
        spt=spt,
        dari_user=pimpinan_user,
        ke_user=penerima,
        status=SPTStatus.DIAJUKAN,
        catatan=catatan
    )


# =========================================================
# KIRIM ULANG SPT REVISI (Pegawai)
# =========================================================
@transaction.atomic
def pegawai_kirim_ulang_revisi(spt: SPT, pegawai_user, kasubbag_user, catatan=""):
    """
    Pegawai mengirim ulang SPT setelah revisi
    """

    # validasi ownership
    if spt.created_by != pegawai_user:
        raise ValueError("Bukan pemilik SPT")

    # hanya bisa kirim ulang jika status revisi
    if spt.status not in ["revisi_kasubbag", "revisi_pegawai"]:
        raise ValueError("SPT belum dalam status revisi")

    # update status SPT
    spt.status = SPTStatus.DIAJUKAN_ULANG
    spt.save()

    template = DisposisiTemplate.objects.get(tipe=DisposisiTipe.REQUEST)
    # buat disposisi baru ke kasubbag
    return Disposisi.objects.create(
        spt=spt,
        dari_user=pegawai_user,
        ke_user=kasubbag_user,
        status=SPTStatus.DIAJUKAN,
        catatan=catatan or template.teks_default or "Mohon di review kembali"
    )
    

@transaction.atomic
def pimpinan_ttd_spt(spt: SPT, pimpinan_user, signature_file=None):
    """
    Pimpinan memberikan tanda tangan pada SPT (final approval)
    """

    # validasi status
    if spt.status != "review_pimpinan":
        raise ValueError("SPT belum masuk tahap pimpinan")

    # validasi role sederhana (optional)
    if not pimpinan_user.groups.filter(name="pimpinan").exists():
        raise ValueError("User bukan pimpinan")

    # update SPT
    spt.status = SPTStatus.DISETUJUI_FINAL
    spt.pimpinan = pimpinan_user

    # jika ada field ttd
    if hasattr(spt, "ttd_pimpinan"):
        spt.ttd_pimpinan = signature_file

    spt.save()

    return spt

@transaction.atomic
def mulai_pelaksanaan_spt(spt: SPT, pegawai_user):
    """
    Pegawai mulai melaksanakan tugas setelah SPT disetujui
    """

    # validasi ownership
    if spt.created_by != pegawai_user:
        raise ValueError("Bukan pemilik SPT")

    # hanya bisa mulai setelah ttd pimpinan
    if spt.status != SPTStatus.DISETUJUI_FINAL:
        raise ValueError("SPT belum disetujui pimpinan")

    # update status
    spt.status = SPTStatus.PELAKSANAAN
    spt.save()

    return spt

# @transaction.atomic
# def upload_laporan_spt(spt: SPT, pegawai_user, file_laporan=None, catatan=""):
#     """
#     Pegawai upload laporan setelah pelaksanaan tugas
#     """

#     # validasi pemilik
#     if spt.created_by != pegawai_user:
#         raise ValueError("Bukan pemilik SPT")

#     # validasi status
#     if spt.status != "pelaksanaan":
#         raise ValueError("SPT belum dalam tahap pelaksanaan")

#     # update status SPT
#     spt.status = "laporan_dikirim"
#     spt.save()

#     # simpan laporan
#     laporan = Laporan.objects.create(
#         spt=spt,
#         uploaded_by=pegawai_user,
#         file=file_laporan,
#         catatan=catatan,
#         status="menunggu_verifikasi"
#     )

#     return laporan


# =============== contoh penggunaan ================
# from .services.spt_service import create_spt

# def create_view(request):
#     if request.method == "POST":
#         create_spt(request.user, request.POST)
#         return redirect("spt_list")

#     return render(request, "pages/create.html")


# -----------------------------------------tambahan
class SPTStateMachine:
    transitions = {
        SPTStatus.DRAFT: {
            "ajukan": "diajukan"
        },
        SPTStatus.PERMOHONAN_DIAJUKAN: {
            "setujui": "disetujui",
            "tolak": "ditolak",
            "revisi": "draft"
        }
    }

    def __init__(self, state):
        self.state = state

    def transition(self, event):
        if event not in self.transitions.get(self.state, {}):
            raise Exception("Aksi tidak valid")

        return self.transitions[self.state][event]
    

@transaction.atomic
def apply_action(spt, event, user):
    from .handlers import handlers
    
    # 1. validasi state
    sm = SPTStateMachine(spt.status)
    new_status = sm.transition(event)

    # 2. ambil handler
    handler = handlers.get(event, None)
    if not handler:
        raise Exception("Event tidak dikenal")

    # 3. jalankan aksi
    handler(spt, user)

    # 4. update state (opsional kalau handler tidak set)
    spt.status = new_status
    spt.save()

    return spt
    
# def ajukan():
#     print("Mengajukan SPT...")

# def setujui():
#     print("Menyetujui SPT...")

# transitions = {
#     "draft": {
#         "ajukan": ("diajukan", ajukan)
#     },
#     "diajukan": {
#         "setujui": ("disetujui", setujui)
#     }
# }

# def apply_action(state, action):
#     if action in transitions.get(state, {}):
#         new_state, func = transitions[state][action]
#         func()  # jalankan fungsi
#         return new_state
#     else:
#         print("Aksi tidak valid")
#         return state


# # contoh
# state = "draft"
# state = apply_action(state, "ajukan")
# print(state)