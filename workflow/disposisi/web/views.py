from django.shortcuts import render

# login
from django.contrib.auth.decorators import login_required

# selectors
from workflow.disposisi.selectors import (
    get_disposisi_by_filter, get_inbox_disposisi,
    get_disposisi_by_id
)

# services
from workflow.disposisi.services import (
    DisposisiServices
)
from spt.spt.services import (
    SPTServices, SPTLampiran, SPTStatus
)

# models
from workflow.models import (
    Disposisi,
    DisposisiTipe
)

# forms
from .forms import (
    SPTForm
)

@login_required
def detail(request, disposisi_id):
    disposisi = get_disposisi_by_id(disposisi_id)
    spt = disposisi.spt
    form = SPTForm(instance=spt)
    context = {
        "disposisi": disposisi,
        "STATUS_DISPOSISI": DisposisiTipe,
        "spt_form": form,
        "spt": spt
    }
    return render(request, "workflow/disposisi/pages/detail.html", context)

# @login_required
# def kirim_revisi(request, disposisi_id):
#     disposisi = get_disposisi_by_id(disposisi_id)
#     DisposisiServices.kirim_revisi(disposisi, request.user)
#     return redirect("workflow_disposisi_web_inbox")

@login_required
def inbox_detail(request, disposisi_id):
    disposisi = get_disposisi_by_id(disposisi_id)
    spt = disposisi.spt
    form = SPTForm(instance=spt)
    context = {
        "disposisi": disposisi,
        "STATUS_DISPOSISI": DisposisiTipe,
        "spt_form": form,
        "spt": spt
    }
    return render(request, "workflow/disposisi/pages/inbox-detail.html", context)

@login_required
def inbox(request):
    context = {
        "disposisi_list": get_inbox_disposisi(request.user),
        "STATUS_DISPOSISI": DisposisiTipe
    }
    return render(request, "workflow/disposisi/pages/inbox.html", context) 

def daftar_disposisi(request):
    qs = get_disposisi_by_filter(ke_user=request.user, status=DisposisiTipe.INSTRUKSI)
    context = {
        "disposisi_list": qs,
        "STATUS_DISPOSISI": DisposisiTipe
    }
    
    return render(request, "workflow/disposisi/list.html", context)