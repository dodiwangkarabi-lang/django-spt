from django.db import transaction
from .models import SPT, Disposisi


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

    if disposisi.status != "diajukan":
        raise ValueError("Disposisi sudah diproses")

    spt = disposisi.spt

    # update disposisi lama
    disposisi.status = "disetujui"
    disposisi.save()

    # update status SPT
    spt.status = "review_pimpinan"
    spt.save()

    return Disposisi.objects.create(
        spt=spt,
        dari_user=kasubbag_user,
        ke_user=pimpinan_user,
        status="diajukan",
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

    if disposisi.status != "diajukan":
        raise ValueError("Disposisi sudah diproses")

    spt = disposisi.spt

    # update disposisi
    disposisi.status = "ditolak"
    disposisi.catatan = catatan
    disposisi.save()

    # update SPT
    spt.status = "ditolak_kasubbag"
    spt.save()

    return spt


# =========================================================
# 3. REVISI (Kasubbag minta perbaikan ke pegawai)
# =========================================================
@transaction.atomic
def kasubbag_revisi(disposisi: Disposisi, kasubbag_user, pegawai_user, catatan=""):
    """
    Kasubbag mengembalikan SPT ke pegawai untuk direvisi
    """

    if disposisi.ke_user != kasubbag_user:
        raise ValueError("Tidak berhak memproses disposisi ini")

    if disposisi.status != "diajukan":
        raise ValueError("Disposisi sudah diproses")

    spt = disposisi.spt

    # update disposisi lama
    disposisi.status = "revisi"
    disposisi.catatan = catatan
    disposisi.save()

    # update SPT
    spt.status = "revisi_kasubbag"
    spt.save()

    # create disposisi balik ke pegawai
    return Disposisi.objects.create(
        spt=spt,
        dari_user=kasubbag_user,
        ke_user=pegawai_user,
        status="diajukan",
        catatan=catatan
    )