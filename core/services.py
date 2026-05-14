from django.db import transaction
from django.db.models import F
from django.utils import timezone

# models
from spt.models import NomorSuratSequence, JenisSurat

@transaction.atomic
def generate_nomor_surat(jenis_surat: JenisSurat, tanggal=None):
    """
    Membuat Nomor Surat Otomatis

    Args:
        jenis_surat (JenisSurat): instace object dari model JenisSurat
        tanggal (datetime, optional): tanggal untuk membuat nomor surat. Defaults to None.

    Returns:
        nomor_surat: string berisi nomor surat
        
    Example:
        >>> jenis_surat = JenisSurat.objects.get(kode="SPT")
        >>> generate_nomor_surat(jenis_surat)
        "001/SPT/04/2023"
        
        >>> generate_nomor_surat(jenis_surat, datetime(2023, 4, 1))
        "001/SPT/04/2023"
    """
    if tanggal:
        now = timezone.make_aware(tanggal)
    else:
        now = timezone.now()
    
    seq, created = NomorSuratSequence.objects.select_for_update().get_or_create(
        jenis_surat=jenis_surat,
        tahun=now.year,
        bulan=now.month,
        defaults={"nomor_akhir": 0}
    )
    
    seq.nomor_akhir = F('nomor_akhir') + 1
    seq.save(update_fields=["nomor_akhir"])
    
    seq.refresh_from_db()
    
    nomor_urut = seq.nomor_akhir
    
    nomor_surat = (
        f"{nomor_urut:03d}/"
        f"{jenis_surat.kode}/"
        f"{now.month:02d}/"
        f"{now.year}"
    )
    
    return nomor_surat