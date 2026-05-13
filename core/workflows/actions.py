from spt.models import SPTStatus

def ajukan(model, user):
    model.status = SPTStatus.DIAJUKAN
    model.dibuat_oleh = user
    model.save()
    
    return model

def setujui(model):
    model.status = SPTStatus.DISETUJUI
    model.save()
    
    return model

def tolak(model, catatan=""):
    """
    Penolakan permohonan

    Args:
        model (obj): instance objek
        

    Returns:
        obj: instance objek
    """
    model.status = SPTStatus.DITOLAK
    model.catatan = catatan
    model.save()
    
    return model

def revisi(model, catatan=""):
    model.status = SPTStatus.REVISI
    model.catatan = catatan
    model.save()
    
    return model

def setujui_permohonan(model):
    model.status = SPTStatus.PERMOHONAN_DISETUJUI_PIMPINAN
    model.save()
    
    return model