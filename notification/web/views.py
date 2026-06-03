from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

# models
from notification.models import Notification

# selectors
from notification.selectors.selectors import (
    get_notification_by_id
)

@login_required
def notification_redirect(request, notifikasi_id):
    # print("-----------")
    # notification = Notification.objects.get(pk=notifikasi_id)
    notification = get_object_or_404(
        Notification,
        pk=notifikasi_id,
        penerima=request.user
    )
    # print(notification)
    # print("-----------")

    # tandai sudah dibaca
    if not notification.is_read:
        notification.is_read = True
        notification.read_at = timezone.now()

        notification.save(
            update_fields=['is_read', 'read_at']
        )
        
    # print("notification target")
    # print(notification.target)

    # redirect ke target object
    return redirect(
        notification.target.get_absolute_url()
    )

def index(request):
    return render(request, 'notification/pages/index.html')

def detail(request, notifikasi_id):
    notifikasi = get_notification_by_id(notifikasi_id)
    context = {
        "notifikasi": notifikasi
    }
    return render(request, 'notification/pages/detail.html', context)