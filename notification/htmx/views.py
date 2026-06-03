from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.services import build_table_context

# selectors
from notification.selectors.selectors import (
    get_notification_by_penerima,
    get_notifications,
    get_notifications_unread,
)

# services
from notification.services.services import (
    NotificationService
)

@login_required
def notifikasi_navbar(request):
    qs_notifications = get_notifications_unread(penerima=request.user) # semua notifikasi
    qs = get_notifications_unread(limit=5, penerima=request.user)
    context = {
        "total_notifikasi": qs_notifications.count(),
        "qs": qs,
    }
    return render(request, 'notification/htmx/notifikasi-navbar.html', context)

@login_required
def list_view(request):
    
    init = request.GET.get("init", "")

    qs = get_notification_by_penerima(request.user)

    columns = [
        {"key": "judul", "label": "Judul"},
        {"key": "created_at", "label": "Tanggal", "tipe": "date"},
        {"key": "pesan", "label": "Pesan"},
    ]

    actions = [
        {
            "key": "read",
            "label": "Lihat",
            "url": "notification:notification_web:notification_redirect",
            "param": "id"
        }
    ]

    filters = {
        "tanggal": "created_at__date",
        "judul": "judul__icontains",
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


def index(request):
    return render(request, 'notification/htmx/index.html')