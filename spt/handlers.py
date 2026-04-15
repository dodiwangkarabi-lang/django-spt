def handle_ajukan(spt, user, **kwargs):
    spt.status = "diajukan"

def handle_setujui(spt, user, **kwargs):
    spt.status = "disetujui"

handlers = {
    "ajukan": handle_ajukan,
    "setujui": handle_setujui,
}