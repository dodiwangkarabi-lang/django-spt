from spt.models import SPTStatus

def ajukan(model, user):
    model.status = SPTStatus.DIAJUKAN
    model.diabuat_oleh = user
    model.save()
    
    return model

def approve(model):
    model.status = SPTStatus.DISETUJUI
    model.save()
    
    return model

def reject(model, catatan=""):
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