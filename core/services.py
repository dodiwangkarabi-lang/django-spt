from django.db import transaction
from django.db.models import F
from django.utils import timezone

from django.core.paginator import Paginator

# models
from spt.models import NomorSuratSequence, JenisSurat

# core/services/table_service.py

from django.core.paginator import Paginator
from django.db.models import Q


def build_table_context(
    request,
    queryset,
    columns,
    actions,
    search_fields=None,
    filters=None,
    per_page=10,
):
    """

    Args:
        request (_type_): _description_
        queryset (QuerySet): _description_
        columns (_type_): _description_
        actions (_type_): _description_
        search_fields (_type_, optional): _description_. Defaults to None.
        filters (_type_, optional): _description_. Defaults to None.
        per_page (int, optional): _description_. Defaults to 10.

    Returns:
        _type_: _description_
        
    Example:
        >>> build_table_context(request, queryset, columns, actions, search_fields, filters)
        
        contoh filter:
        
        filters = {
            "tanggal": "created_at__date",
            "status": "status",
            "pegawai": "pegawai_id",
        }
        
        filters = {
            "tanggal_awal": "created_at__date__gte",
            "tanggal_akhir": "created_at__date__lte",
            "status": "status",
        }
        
        columns = [
            {"key": "created_at", "label": "Tanggal", "tipe": "date"},
            {"key": "status", "label": "Status"},
        ]
        
        actions = [
            {
                "key": "detail",
                "label": "Detail",
                "url": "disposisi_detail",
                "param": "id",
            },
        ]

    """
    q = request.GET.get("q", "")
    page_number = request.GET.get("page")

    # search
    if q and search_fields:
        query = Q()

        for field in search_fields:
            query |= Q(**{f"{field}__icontains": q})

        queryset = queryset.filter(query)

    # dynamic filters
    if filters:
        for param_name, lookup in filters.items():
            value = request.GET.get(param_name)

            if value:
                queryset = queryset.filter(**{lookup: value})

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(page_number)

    return {
        "page_obj": page_obj,
        "columns": columns,
        "actions": actions,
    }

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