from spt.models import SPT, SPTStatus, SPTLampiran

def update_spt(spt: SPT, **kwargs):
    for key, value in kwargs.items():
        setattr(spt, key, value)
    spt.save()
    return spt

def submit_spt(spt: SPT):
    spt.status = SPTStatus.DIAJUKAN
    spt.save()
    return spt