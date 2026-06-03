from django.db import transaction

# models
from notification.models import Notification

# constants
from notification.constants.constants import NotificationEventType

# selectors
from notification.selectors.selectors import get_notification_by_id

class NotificationEventService:
    
    @staticmethod
    def create_notification(event: str, payload: dict):
        """
        Event: string (event_type)
            
            contoh: NotificationEventType.SPT_CREATED
            
            contoh: NotificationEventType.DISPOSISI_CREATED
            
        payload: dict berisi data konteks
        
        Example:
            >>> payload = {
                "penerima": User.objects.get(id=1),
                "pengirim": User.objects.get(id=2),
                "spt": SPT.objects.get(id=1),
                "disposisi": Disposisi.objects.get(id=1),
                "permohonan": PermohonanSPT.objects.get(id=1),
                "judul": "Judul Notifikasi",
                "pesan": "Pesan Notifikasi"
            }
            
            >>> event = "disposisi_diajukan"
        """

        penerima = payload.get("penerima")
        pengirim = payload.get("pengirim")

        spt = payload.get("spt")
        disposisi = payload.get("disposisi")
        permohonan = payload.get("permohonan")

        judul = payload.get("judul", "Notifikasi Sistem")
        pesan = payload.get("pesan", "")

        # validasi minimal
        if not penerima:
            raise ValueError("penerima wajib diisi")

        notification = Notification.objects.create(
            penerima=penerima,
            pengirim=pengirim,
            spt=spt,
            disposisi=disposisi,
            permohonan=permohonan,
            event_type=event,
            judul=judul,
            pesan=pesan
        )

        return notification
    
    @staticmethod
    def createEvent(event_type):
        pass
    
class NotificationService:
    
    @staticmethod
    def sudah_dibaca(notifikasi_id):
        notifikasi = get_notification_by_id(notifikasi_id)
        notifikasi.is_read = True
        notifikasi.save()
        return notifikasi
    
    @staticmethod
    @transaction.atomic
    def kirim_pesan(*, pengirim, daftar_penerima=[], data_notifikasi={}):
        """
        kirim pesan

        Args:
            pengirim (_type_): _description_
            daftar_penerima (list, optional): _description_. Defaults to [].
            data_notifikasi (dict, optional): _description_. Defaults to {}.

        Returns:
            _type_: _description_
            
        Example:
            >>> data_notifikasi = {
                "pesan": f"Pengajuan Permohonan Kegiatan '{permohonan.judul}'",
                "content_type": ContentType.objects.get_for_model(PermohonanSPT),
                "object_id": permohonan.id,
                "event_type": NotificationEventType.PERMOHONAN_CREATED,
                "judul": "Pengajuan Permohonan Kegiatan"
            }
        """
        for penerima in daftar_penerima:
            data_notifikasi["penerima"] = penerima
            data_notifikasi["pengirim"] = pengirim
            NotificationService.create(data_notifikasi)
        
        return True
    
    @staticmethod
    def create(data):
        """
        Buat / Kirim Notifikasi

        Args:
            data (_type_): _description_

        Returns:
            _type_: _description_
            
        Example:
            >>> data_notifikasi = {
                    "penerima": get_pimpinan_user(),
                    "pengirim": get_kasubag_user(),
                    "pesan": f"Pengajuan Permohonan Kegiatan '{permohonan.judul}'",
                    "content_type": ContentType.objects.get_for_model(PermohonanSPT),
                    "object_id": permohonan.id,
                    "event_type": NotificationEventType.PERMOHONAN_CREATED,
                    "judul": "Pengajuan Permohonan Kegiatan"
                }
        """
        notifikasi = Notification.objects.create(**data)
        return notifikasi