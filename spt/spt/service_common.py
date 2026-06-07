from django.db import transaction

# models
from spt.models import (
    SPT, SPTLampiran, SPTStatus, JenisSurat
)

# services
from core.services import generate_nomor_surat

class SPTServices:
    
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
    
    
    