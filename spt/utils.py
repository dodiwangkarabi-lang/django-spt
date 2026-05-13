# utils/nomor_surat.py
from datetime import datetime, date
from .models import NomorSuratSequence
from django.db import transaction

ROMAWI = {
    1: "I", 2: "II", 3: "III", 4: "IV",
    5: "V", 6: "VI", 7: "VII", 8: "VIII",
    9: "IX", 10: "X", 11: "XI", 12: "XII"
}

def generate_nomor_surat(model):
    today = date.today()
    tahun = today.year
    bulan = today.month

    with transaction.atomic():
        seq, created = model.objects.select_for_update().get_or_create(
            tahun=tahun,
            bulan=bulan,
            defaults={"nomor_terakhir": 0}
        )

        seq.nomor_terakhir += 1
        seq.save()

        nomor_urut = str(seq.nomor_terakhir).zfill(3)  # 001, 002, dst
        bulan_romawi = ROMAWI[bulan]

        nomor_surat = f"090/{nomor_urut}/SPT/{bulan_romawi}/{tahun}"
        return nomor_surat
      

# ROMAWI = {
#     1: "I", 2: "II", 3: "III", 4: "IV",
#     5: "V", 6: "VI", 7: "VII", 8: "VIII",
#     9: "IX", 10: "X", 11: "XI", 12: "XII"
# }

def generate_nomor_spt():
    now = datetime.now()
    tahun = now.year
    bulan = now.month

    with transaction.atomic():
        seq, created = NomorSuratSequence.objects.select_for_update().get_or_create(
            tahun=tahun,
            bulan=bulan,
            defaults={"nomor_akhir": 0}
        )

        seq.nomor_akhir += 1
        seq.save()

        nomor_urut = str(seq.nomor_akhir).zfill(3)

    # nomor = f"800/{nomor_urut}/SPT-SATUI/{ROMAWI[bulan]}/{tahun}"
    nomor = f"SPT/{nomor_urut}/{ROMAWI[bulan]}/{tahun}"
    return nomor