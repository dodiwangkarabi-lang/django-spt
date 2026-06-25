from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

# services
from core.services import generate_nomor_surat
from workflow.disposisi.services import DisposisiServices
from accounts.services.auth_service import UserService
from notification.services.services import NotificationService

# selectors
from accounts.selectors.selectors import (
    get_pimpinan_user, get_kasubag_user, get_pegawai_user
)

# models
# model user
from django.contrib.auth.models import User
from spt.models import (
    SPT, SPTLampiran, SPTStatus, JenisSurat
)
from workflow.models import (
    Disposisi, DisposisiTipe
)
from notification.models import (
    Notification
)

# constants
from notification.constants.constants import (
    NotificationEventType
)

class LampiranServices:
    
    @staticmethod
    @transaction.atomic
    def hapus_lampiran(*, lampiran_id):
        lampiran = get_object_or_404(SPTLampiran, id=lampiran_id)
        lampiran.delete()
        return lampiran
    
    @staticmethod
    @transaction.atomic
    def simpan_banyak_lampiran(*, spt, files):
        """
        simpan banyak lampiran

        Args:
            spt (_type_): _description_
            files (_type_): _description_

        Returns:
            _type_: _description_
        
        Example:
            >>> LampiranServices.simpan_banyak_lampiran(spt=spt, files=files)
            
        Contoh Data:
            >>> spt = SPT.objects.get(id=1)
            >>> files = request.FILES.getlist("lampiran")
            >>> LampiranServices.simpan_banyak_lampiran(spt=spt, files=files)
            
        """
        for file in files:
            SPTLampiran.objects.create(spt=spt, file=file)

        return True

class SPTServices:
    
    @staticmethod
    @transaction.atomic
    def kirim_revisi_spt(*, data_spt: dict, spt):
        # print("data spt")
        # print(data_spt)
        
        data_spt["dibuat_oleh"] = User.objects.get(id=data_spt["dibuat_oleh"])
        
        pimpinan_user = get_pimpinan_user()
        kasubag_user = get_kasubag_user()
        
        data_spt = data_spt.copy()
        data_spt["status"] = SPTStatus.DIAJUKAN
        
        for key, value in data_spt.items():
            setattr(spt, key, value)

        spt.save()
        
        disposisi = Disposisi.objects.get(spt=spt)
        disposisi.dari_user = kasubag_user
        disposisi.ke_user = pimpinan_user
        disposisi.status = DisposisiTipe.REQUEST
        disposisi.save()
        
        # notifikasi
        data_notification = {
            "pesan": f"Revisi SPT: {spt.judul}",
            "content_type": ContentType.objects.get_for_model(Disposisi),
            "object_id": disposisi.id,
            "event_type": NotificationEventType.SPT_SUBMITTED,
            "judul": "Pengajuan Revisi SPT"
        }
        
        NotificationService.kirim_pesan(
            pengirim = get_kasubag_user(),
            daftar_penerima = [get_pimpinan_user()],
            data_notifikasi = data_notification
        )
        
        return spt
    
    @staticmethod
    @transaction.atomic
    def save_tanpa_lampiran(*, data_spt: dict, spt=None):
        """
        simpan atau update data

        Args:
            data_spt (dict): _description_
            spt (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
            
        Example:
            >>> SPTServices.save_tanpa_lampiran(data_spt=data_spt, spt=spt)
            
        Contoh Data:
            >>> data_spt = {
                "nomor_spt": "SPT/2021/0001",
                "judul": "Judul SPT",
                "tanggal": "2021-01-01",
                "jenis_surat": "1",
            }
            >>> spt = SPT.objects.get(id=1)
            >>> SPTServices.save_tanpa_lampiran(data_spt=data_spt, spt=spt)
        """
        # =========================
        # UPDATE / CREATE SPT
        # =========================

        if spt is None:
            spt = SPT.objects.create(**data_spt)

        else:
            for key, value in data_spt.items():
                setattr(spt, key, value)

            spt.save()

        return spt
    
    @staticmethod
    @transaction.atomic
    def save_dengan_lampiran(*, data_spt: dict, data_lampiran: list, spt=None):
        """
        simpan atau update data

        Args:
            data_spt (dict): _description_
            data_lampiran (list): _description_
            spt (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
            
        Example:
            >>> SPTServices.save_dengan_lampiran(data_spt=data_spt, data_lampiran=data_lampiran, spt=spt)
            
        Contoh Data:
            >>> data_spt = {
                "nomor_spt": "SPT/2021/0001",
                "judul": "Judul SPT",
                "deskripsi": "Deskripsi SPT",
                "tanggal_mulai": "2021-01-01",
                "tanggal_selesai": "2021-01-31",
                "dibuat_oleh": user.id,
            }

            >>> data_lampiran = [
                {
                    "file": file,
                    "keterangan": "Keterangan lampiran 1",
                },
                {
                    "file": file,
                    "keterangan": "Keterangan lampiran 2",
                }
            ]
        """
        # =========================
        # UPDATE / CREATE SPT
        # =========================

        if spt is None:
            jenis_surat = JenisSurat.objects.get(kode="SPT")
            data_spt["nomor_spt"] = generate_nomor_surat(jenis_surat=jenis_surat)
            spt = SPT.objects.create(**data_spt)

        else:
            for key, value in data_spt.items():
                setattr(spt, key, value)

            spt.save()

        # =========================
        # LAMPIRAN
        # =========================

        lampiran_ids = []

        for item in data_lampiran:

            lampiran_id = item.get('id')

            if lampiran_id:

                # UPDATE
                lampiran = SPTLampiran.objects.get(
                    id=lampiran_id,
                    spt=spt
                )
                
                for key, value in item.items():

                    if key != 'id':
                        setattr(lampiran, key, value)

                lampiran.save()

            else:

                # CREATE
                lampiran = SPTLampiran.objects.create(
                    spt=spt,
                    **item
                )

            lampiran_ids.append(lampiran.id)

        # =========================
        # DELETE YANG TIDAK ADA
        # =========================

        spt.lampiran.exclude(
            id__in=lampiran_ids
        ).delete()

        return spt
    
    
    @staticmethod
    @transaction.atomic
    def update_spt(spt, **kwargs):
        # update banyak field
        for field in kwargs.keys():
            setattr(spt, field, kwargs[field])
        
        spt.save()
        
        return spt
    
    def _update_disposisi(spt, catatan=""):
        # update disposisi
        disposisi = Disposisi.objects.get(spt=spt)
        kasubag = get_kasubag_user()
        service = DisposisiServices.update_status_dan_perima(
            disposisi=disposisi,
            status=DisposisiTipe.INSTRUKSI,
            penerima_user=kasubag,
            catatan=catatan
        )
    
    @staticmethod
    @transaction.atomic
    def tolak_spt(spt, catatan=""):
        spt.status = SPTStatus.DITOLAK
        spt.catatan = catatan
        spt.save()
        
        # update disposisi
        SPTServices._update_disposisi(spt, catatan="")
        
        # kirim notifikasi
        data_notifikasi = {
            "pesan": f"SPT Ditolak '{spt.judul}'",
            "content_type": ContentType.objects.get_for_model(SPT),
            "object_id": spt.id,
            "event_type": NotificationEventType.SPT_REJECTED,
            "judul": "Penolakan SPT"
        }
        
        pegawai = spt.dibuat_oleh
        
        NotificationService.kirim_pesan(
            pengirim=get_pimpinan_user(),
            daftar_penerima = [get_kasubag_user(), pegawai],
            data_notifikasi=data_notifikasi
        )
        
        return spt
    
    @staticmethod
    @transaction.atomic
    def terima_spt(spt, catatan=""):
        """
        Terima SPT
        
        terdapat juga kirim pesan

        Args:
            spt (_type_): _description_
            catatan (str, optional): _description_. Defaults to "".

        Returns:
            _type_: _description_
        """
        spt.status = SPTStatus.DISETUJUI
        spt.catatan = catatan
        spt.save()
        
        # kirim notifikasi
        data_notifikasi = {
            "pesan": f"SPT Diterima '{spt.judul}'",
            "content_type": ContentType.objects.get_for_model(SPT),
            "object_id": spt.id,
            "event_type": NotificationEventType.SPT_REJECTED,
            "judul": "Penerimaan SPT"
        }
        
        pegawai = spt.dibuat_oleh
        
        NotificationService.kirim_pesan(
            pengirim=get_pimpinan_user(),
            daftar_penerima = [get_kasubag_user(), pegawai],
            data_notifikasi=data_notifikasi
        )
        
        # update disposisi
        SPTServices._update_disposisi(spt, catatan="")
        
        return spt
    
    # @staticmethod
    # @transaction.atomic
    # def create_or_update_spt(spt, **kwargs):
    #     pass
    
    @staticmethod
    @transaction.atomic
    def revisi_spt(spt, catatan=""):
        spt.status = SPTStatus.REVISI
        spt.catatan = catatan
        spt.save()
        
        # update disposisi
        SPTServices._update_disposisi(spt, catatan="")
        
        # kirim notifikasi
        data_notifikasi = {
            "pesan": f"SPT perlu revisi '{spt.judul}'",
            "content_type": ContentType.objects.get_for_model(SPT),
            "object_id": spt.id,
            "event_type": NotificationEventType.SPT_REJECTED,
            "judul": "Revisi SPT"
        }
        
        pegawai = spt.dibuat_oleh
        
        NotificationService.kirim_pesan(
            pengirim=get_pimpinan_user(),
            daftar_penerima = [get_kasubag_user(), pegawai],
            data_notifikasi=data_notifikasi
        )
        
        return spt
    
    @staticmethod
    @transaction.atomic
    def buat_spt_dan_disposisi_baru(data: dict, user, lampiran=[]):
        """
        Buat Spt dan Disposisi Baru

        Args:
            data (dict): data utama untuk spt
            user (obj): instance object User
            lampiran (list, optional): daftar lampiran. Defaults to [].

        Returns:
            obj: instance object SPT
            
        Example:
            >>> lampiran = request.FILES.getlist("lampiran")
            >>> spt = SPTServices.buat_spt_dan_disposisi_baru(data=data, user=user, lampiran=lampiran)
        """
        jenis_surat = JenisSurat.objects.get(kode="SPT")
        data["nomor_spt"] = generate_nomor_surat(jenis_surat=jenis_surat)
        spt = SPT.objects.create(**data)
        
        disposisi = DisposisiServices.create_disposisi_baru(spt=spt, user=user)
        
        # lampiran pakai bulk
        for l in lampiran:
            SPTLampiran.objects.create(spt=spt, file=l)
        
        return spt
    
    @staticmethod
    @transaction.atomic
    def create_spt_with_disposisi(data: dict, disposisi, lampiran=[]):
        jenis_surat = JenisSurat.objects.get(kode="SPT")
        data["nomor_spt"] = generate_nomor_surat(jenis_surat=jenis_surat)
        spt = SPT.objects.create(**data)
                
        pimpinan = get_pimpinan_user()
        disposisi.spt = spt
        if pimpinan:
            disposisi.ke_user = pimpinan
            disposisi.status = DisposisiTipe.REQUEST
        disposisi.save()
        
        # DisposisiServices.update_penerima(disposisi, disposisi.ke_user)
        
        # lampiran pakai bulk
        for l in lampiran:
            SPTLampiran.objects.create(spt=spt, file=l)
            
        # notifikasi
        data_notification = {
            "pesan": f"SPT: {spt.judul}",
            "content_type": ContentType.objects.get_for_model(Disposisi),
            "object_id": disposisi.id,
            "event_type": NotificationEventType.SPT_CREATED,
            "judul": "Pengajuan SPT"
        }
        
        NotificationService.kirim_pesan(
            pengirim = get_kasubag_user(),
            daftar_penerima = [get_pimpinan_user()],
            data_notifikasi = data_notification
        )
        
        return spt
    
    @staticmethod
    @transaction.atomic
    def update_spt_with_disposisi(data: dict, disposisi, lampiran=[]):
        # jenis_surat = JenisSurat.objects.get(kode="SPT")
        # data["nomor_spt"] = generate_nomor_surat(jenis_surat=jenis_surat)
        # spt = SPT.objects.update(**data)
        spt = disposisi.spt
        
        for field, value in data.items():
            setattr(spt, field, value)
        spt.save()
        
        # print("spt sekarang", spt)
                
        pimpinan = get_pimpinan_user()
        disposisi.spt = spt
        if pimpinan:
            disposisi.ke_user = pimpinan
            disposisi.status = DisposisiTipe.REQUEST
        disposisi.save()
        
        # DisposisiServices.update_penerima(disposisi, disposisi.ke_user)
        
        if lampiran:
            # hapus dulu semua lampiran
            SPTLampiran.objects.filter(spt=spt).delete()
        
        # lampiran pakai bulk
        for l in lampiran:
            SPTLampiran.objects.create(spt=spt, file=l)
            
        # notifikasi
        data_notification = {
            "pesan": f"SPT: {spt.judul}",
            "content_type": ContentType.objects.get_for_model(Disposisi),
            "object_id": disposisi.id,
            "event_type": NotificationEventType.SPT_CREATED,
            "judul": "Pengajuan SPT"
        }
        
        NotificationService.kirim_pesan(
            pengirim = get_kasubag_user(),
            daftar_penerima = [get_pimpinan_user()],
            data_notifikasi = data_notification
        )
        
        return spt
    
    @staticmethod
    @transaction.atomic
    def update_status(spt, status):
        spt.status = status
        spt.save()
        
        return spt
    
    @staticmethod
    def create(**kwargs):
        spt = SPT.objects.create(**kwargs)
        
        return spt