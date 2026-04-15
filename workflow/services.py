class SPTWorkflowService:

    def __init__(self, user):
        self.user = user
        
    def execute(self, spt, action, note=None):
        current_state = spt.status

        next_state = self._get_next_state(current_state, action)

        if not next_state:
            raise ValueError(f"Aksi '{action}' tidak valid untuk state '{current_state}'")

        old_state = spt.status
        spt.status = next_state
        spt.save()

        self._log(spt, action, old_state, next_state, note)

        return spt
    
    def _get_next_state(self, current, action):
        WORKFLOW = {
            "draft": {
                "submit": "permohonan_diajukan"
            },

            "permohonan_diajukan": {
                "approve": "kasubag_review",
                "reject": "ditolak",
            },

            "kasubag_review": {
                "approve": "kasubag_setujui",
                "reject": "ditolak",
            },

            "kasubag_setujui": {
                "forward": "kepala_review_permohonan"
            },

            "kepala_review_permohonan": {
                "approve": "kepala_setujui_permohonan",
                "reject": "ditolak",
            },

            "kepala_setujui_permohonan": {
                "generate_spt": "spt_dibuat"
            },

            "spt_dibuat": {
                "review_spt": "kepala_review_spt"
            },

            "kepala_review_spt": {
                "approve_spt": "kepala_setujui_spt",
                "reject_spt": "ditolak",
            },

            "kepala_setujui_spt": {
                "sign": "ttd_spt"
            },

            "ttd_spt": {
                "finalize": "selesai"
            }
        }

        return WORKFLOW.get(current, {}).get(action)
    
    def _log(self, spt, action, from_state, to_state, note):
        SPTWorkflowLog.objects.create(
            spt=spt,
            actor=self.user,
            action=action,
            from_status=from_state,
            to_status=to_state,
            note=note
        )
        
class SPTDocumentService:

    def generate_spt(self, permohonan):
        # logic generate nomor, template, dll
        spt = SPT.objects.create(
            pemohon=permohonan.pemohon,
            judul=permohonan.judul,
            tujuan=permohonan.tujuan,
            status="spt_dibuat"
        )
        return spt
    
class SPTSigningService:

    def sign(self, spt, user):
        if spt.status != "kepala_setujui_spt":
            raise ValueError("SPT belum siap ditandatangani")

        spt.status = "ttd_spt"
        spt.save()

        return spt
    
    
# contoh penggunaan di view
# def approve_spt(request, id):
#     spt = SPT.objects.get(id=id)

#     service = SPTWorkflowService(user=request.user)
#     spt = service.execute(spt, action="approve", note="Disetujui")

#     return Response({"status": spt.status})