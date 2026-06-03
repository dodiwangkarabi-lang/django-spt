from django.db.models import Q, F
from django.db.models.query import QuerySet

# models
from workflow.models import Disposisi, DisposisiTipe

def get_inbox_disposisi(user):
    return (
        Disposisi.objects
        .filter(
            Q(ke_user=user) & (Q(status=DisposisiTipe.INSTRUKSI) | Q(status=DisposisiTipe.REQUEST))
        )
        # .select_related('spt')
        .order_by('-created_at')
    )

def get_disposisi_by_filter(**kwargs) -> QuerySet:
    qs = Disposisi.objects.filter(**kwargs)
    qs = qs.order_by('-created_at')
    return qs

def get_disposisi() -> QuerySet:
    return Disposisi.objects.all()

def get_disposisi_by_id(id):
    return Disposisi.objects.get(id=id)