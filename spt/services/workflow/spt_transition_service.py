# services/workflow/spt_transition_service.py

# from spt.constants.spt_status import SPTStatus
from spt.exceptions.workflow_exception import InvalidTransition

from spt.models import SPTStatus

ALLOWED_TRANSITIONS = {
    SPTStatus.DRAFT: [
        SPTStatus.PERMOHONAN_DIAJUKAN,
    ],
    
    SPTStatus.PERMOHONAN_DIAJUKAN: [
        SPTStatus.KASUBAG_SETUJUI_PERMOHOAN,
        SPTStatus.KASUBAG_REVIEW
    ],

    SPTStatus.DIAJUKAN: [
        SPTStatus.DISETUJUI,
        SPTStatus.DITOLAK,
    ],

    SPTStatus.DITOLAK: [
        SPTStatus.DRAFT,
    ],

    SPTStatus.DISETUJUI: [
        SPTStatus.SELESAI,
    ],

    SPTStatus.SELESAI: [],
}


def can_transition(current_status, new_status):
    allowed = ALLOWED_TRANSITIONS.get(current_status, [])
    return new_status in allowed


def transition_spt(spt, new_status):

    if not can_transition(spt.status, new_status):
        raise InvalidTransition(
            f"Tidak bisa pindah dari "
            f"{spt.status} ke {new_status}"
        )

    spt.status = new_status
    spt.save(update_fields=["status"])

    return spt