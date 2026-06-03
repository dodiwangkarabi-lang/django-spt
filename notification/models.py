from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# class Notification(models.Model):
#     penerima = models.ForeignKey(User, on_delete=models.CASCADE)

#     # polymorphic target
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveBigIntegerField()
#     target = GenericForeignKey('content_type', 'object_id')

#     pesan = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     is_read = models.BooleanField(default=False)

class Notification(models.Model):
    penerima = models.ForeignKey(User, on_delete=models.CASCADE)

    pengirim = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sent_notifications"
    )
    
    # === INI PENGGANTI spt/disposisi/permohonan ===
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')
    
    event_type = models.CharField(max_length=50, null=True, blank=True)

    judul = models.CharField(max_length=255)
    pesan = models.TextField()

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.pk} Notifikasi"