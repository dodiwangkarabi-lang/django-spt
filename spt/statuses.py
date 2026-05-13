from spt.models import SPTStatus

def is_draft(spt):
    return spt.status == SPTStatus.DRAFT

def is_permohonan_diajukan(spt):
    return spt.status == SPTStatus.PERMOHONAN_DIAJUKAN

def is_diajukan(spt):
    return spt.status == SPTStatus.DIAJUKAN

def is_revisi_kasubag(spt):
    return spt.status == SPTStatus.REVISI_KASUBAG