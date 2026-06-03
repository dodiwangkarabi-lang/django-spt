from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.services import build_table_context

# selectors
from spt.permohonan.selectors import (
    get_permohonan
)

@login_required
def list_permohonan_view(request):
    
    init = request.GET.get("init", "")

    qs = get_permohonan()

    columns = [
        {"key": "judul", "label": "Judul"},
        {"key": "created_at", "label": "Tanggal", "tipe": "date"},
        {"key": "status", "label": "Status"},
    ]

    actions = [
        {
            "key": "detail",
            "label": "Detail",
            "url": "permohonan:permohonan_web:detail",
            "param": "id",
        },
    ]

    filters = {
        "tanggal": "created_at__date",
        "status": "status",
        "pegawai": "pegawai_id",
    }

    context = build_table_context(
        request=request,
        queryset=qs,
        columns=columns,
        actions=actions,
        search_fields=["judul"],
        filters=filters,
    )

    template = (
        "core/components/table/table.html"
        if init
        else "core/components/table/_table.html"
    )
    

    return render(request, template, context)