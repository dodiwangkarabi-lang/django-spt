# models
from spt.models import PermohonanSPT, LampiranPermohonanSPT

from django.db import transaction

# status
from spt.models import SPTStatus


class PermohonanService:
    
    @staticmethod
    @transaction.atomic
    def update_status(permohonan_id: int, status: str):
        permohonan = PermohonanSPT.objects.get(id=permohonan_id)
        permohonan.status = status
        permohonan.save()
        return permohonan

    @staticmethod
    @transaction.atomic
    def create_permohonan_with_lampiran(
        data_permohonan: dict,
        daftar_lampiran: list
    ):
        permohonan = PermohonanSPT.objects.create(
            **{
                **data_permohonan, 
                "status": SPTStatus.PERMOHONAN_DIAJUKAN
            }
        )

        lampiran_objects = []

        for item in daftar_lampiran:
            lampiran_objects.append(
                LampiranPermohonanSPT(
                    permohonan_spt=permohonan,
                    file=item['file'],
                    keterangan=item['keterangan'] or ""
                )
            )

        LampiranPermohonanSPT.objects.bulk_create(
            lampiran_objects
        )

        return permohonan
    
    @staticmethod
    @transaction.atomic
    def update_permohonan_with_lampiran(
        permohonan_id: int,
        data_permohonan: dict,
        daftar_lampiran
    ):
        pass
        # siswa.nama = nama
        # siswa.save()

        # siswa.nilai.all().delete()

        # nilai_objects = [
        #     Nilai(
        #         siswa=siswa,
        #         mata_kuliah=item["mata_kuliah"],
        #         nilai=item["nilai"]
        #     )
        #     for item in daftar_nilai
        # ]

        # Nilai.objects.bulk_create(
        #     nilai_objects
        # )

        # return siswa