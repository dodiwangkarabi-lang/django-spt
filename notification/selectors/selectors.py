from django.shortcuts import get_object_or_404

# models
from notification.models import Notification
from django.contrib.auth.models import User

def get_notifications():
    return Notification.objects.all()

def get_notification_by_id(id):
    return get_object_or_404(Notification, id=id)

def get_notification_by_penerima(penerima: User):
    return Notification.objects.filter(penerima=penerima)

def get_notifications_unread(*, limit=None, penerima=None):
    qs = Notification.objects.filter(is_read=False)
    if penerima:
        qs = qs.filter(penerima=penerima)
    
    if limit:
        qs = qs[:limit]
        
    return qs