# notification/constants.py

class NotificationEventType:
    # SPT
    SPT_CREATED = "spt.created"
    SPT_SUBMITTED = "spt.submitted"
    SPT_APPROVED = "spt.approved"
    SPT_REJECTED = "spt.rejected"
    SPT_REVISION_REQUESTED = "spt.revision_requested"

    # Disposisi
    DISPOSISI_CREATED = "disposisi.created"
    DISPOSISI_ASSIGNED = "disposisi.assigned"

    # Permohonan
    PERMOHONAN_CREATED = "permohonan.created"
    PERMOHONAN_APPROVED = "permohonan.approved"
    PERMOHONAN_REJECTED = "permohonan.rejected"

    # General
    SYSTEM = "system.event"