from django.shortcuts import get_object_or_404
from workflow.models import Disposisi

def get_disposisi(spt_id):
    disposisi = get_object_or_404(Disposisi, spt_id=spt_id)
    return disposisi

def create_disposisi(spt, dari_user, ke_user, status='diajukan', catatan=''):
    return Disposisi.objects.create(
        spt=spt,
        dari_user=dari_user,
        ke_user=ke_user,
        status=status,
        catatan=catatan
    )

def update_status_disposisi(disposisi, status, catatan=None):
    disposisi.status = status

    if catatan is not None:
        disposisi.catatan = catatan

    disposisi.save()
    return disposisi

def forward_disposisi(disposisi, from_user, to_user, catatan=''):
    # tandai disposisi lama selesai
    disposisi.status = 'disetujui'
    disposisi.save()

    # buat disposisi baru
    return Disposisi.objects.create(
        spt=disposisi.spt,
        dari_user=from_user,
        ke_user=to_user,
        status='diajukan',
        catatan=catatan
    )
    
def get_disposisi_by_spt(spt):
    return Disposisi.objects.filter(spt=spt).order_by('-created_at')

def get_inbox_disposisi(user):
    return Disposisi.objects.filter(
        ke_user=user,
        status='diajukan'
    ).order_by('-created_at')
    
def get_outbox_disposisi(user):
    return Disposisi.objects.filter(
        dari_user=user
    ).order_by('-created_at')
    
def can_user_process_disposisi(user, disposisi):
    return disposisi.ke_user == user and disposisi.status == 'diajukan'

def get_spt_timeline(spt):
    return Disposisi.objects.filter(spt=spt).select_related(
        'dari_user', 'ke_user'
    ).order_by('created_at')
    
    
    
# kasubag
def kasubbag_review_spt(disposisi, kasubbag_user, catatan=''):
    """
    Kasubbag melakukan review awal
    """
    if disposisi.ke_user != kasubbag_user:
        raise PermissionError("User tidak berhak mereview disposisi ini")

    disposisi.status = 'disetujui'
    disposisi.catatan = catatan
    disposisi.save()

    return disposisi

def forward_to_pimpinan(disposisi, kasubbag_user, pimpinan_user, catatan=''):
    """
    Setelah review kasubbag, diteruskan ke pimpinan
    """

    if disposisi.ke_user != kasubbag_user:
        raise PermissionError("Bukan disposisi untuk kasubbag ini")

    # tutup disposisi lama
    disposisi.status = 'disetujui'
    disposisi.save()

    # buat disposisi baru untuk pimpinan
    return Disposisi.objects.create(
        spt=disposisi.spt,
        dari_user=kasubbag_user,
        ke_user=pimpinan_user,
        status='diajukan',
        catatan=catatan
    )
    
def pimpinan_approve_spt(disposisi, pimpinan_user, catatan=''):
    """
    Pimpinan melakukan approval final
    """

    if disposisi.ke_user != pimpinan_user:
        raise PermissionError("User tidak berhak approve")

    disposisi.status = 'disetujui'
    disposisi.catatan = catatan
    disposisi.save()

    # OPTIONAL: update SPT status kalau kamu punya field status di SPT
    # disposisi.spt.status = 'disetujui'
    # disposisi.spt.save()

    return disposisi
