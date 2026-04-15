from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.http import QueryDict
from spt.forms import SPTForm, SPTLampiranFormSet, SPTForm2
import random
from spt.models import SPT, SPTLampiran
from django.http import HttpResponseNotAllowed, HttpResponse, FileResponse
from django.contrib.auth.models import User

from datetime import timedelta


from .services import (
    upload_lampiran_spt, delete_lampiran_spt,
    generate_spt_pdf,
    get_spt_list
)

# def index(request):
#     return render(request, 'spt/index.html')

def spt_action(request, spt_id):
    spt = get_object_or_404(SPT, id=spt_id)
    event = request.POST.get('event')
    
    
    
    return render(request, 'spt/spt_action.html')

def index(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data["nomor_spt"] = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        data["status"] = "diajukan"
        data["dibuat_oleh"] = request.user or None
        form_spt = SPTForm(data)
        if form_spt.is_valid():
            form_spt.save()
            return redirect(reverse('spt_index'))
        
    else:
        form_spt = SPTForm()
        
    context = {
        'form_spt': form_spt
    }
        
    return render(request, 'spt/index.html', context)

def detail(request, spt_id):
    spt = SPT.objects.get(id=spt_id)
    spt_form = SPTForm(instance=spt)
    context = {
        'spt_form': spt_form
    }
    return render(request, 'spt/detail.html', context)

def remove(request, spt_id):
    if request.method != 'POST':
        spt = SPT.objects.get(id=spt_id)
        spt.delete()
        return redirect(reverse('spt_index'))
    return HttpResponseNotAllowed(['POST'])
    

def revisi(request, spt_id):
    return render(request, 'spt/revisi.html')

def verifikasi(request, spt_id):
    return render(request, 'spt/verifikasi.html')

def approve_final(request, spt_id):
    return render(request, 'spt/approve_final')

def ttd(request, spt_id):
    return render(request, 'spt/ttd')

def review(request):
    params = request.GET
    return render(request, 'spt/review.html')

def dashboard(request):
    return render(request, 'core/dashboard.html')

def upload_lampiran(request, spt_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    data = {
        'file': request.FILES.get('file'),
        'keterangan': request.POST.get('keterangan')
    }
    
    upload_lampiran_spt(spt_id=spt_id, data=data)
    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    
    return redirect(reverse('spt_index'))

def delete_lampiran(request, lampiran_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    
    delete_lampiran_spt(lampiran_id=lampiran_id)
    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    
    return redirect(reverse('spt_index'))

def cetak(request, spt_id):
    spt = SPT.objects.get(id=spt_id)
    pdf_bytes = generate_spt_pdf(spt)
    
    # response = HttpResponse(pdf_bytes, content_type='application/pdf')
    # response['Content-Disposition'] = 'inline; filename="spt.pdf"'
    # response['as_attachment'] = False
    
    return FileResponse(
        pdf_bytes,
        content_type='application/pdf',
        as_attachment=False,  # penting!
        filename='spt.pdf'
    )
    
    # inline -> tampil di browser
    # attachment -> langsung download
    
    # kalau mau simpan di db
    # pdf_bytes = generate_spt_pdf_bytes(spt)
    # spt.file_final.save("spt.pdf", ContentFile(pdf_bytes))
    
    # return response
    # return render(request, 'spt/cetak.html')

def preview(request, spt_id):
    spt = SPT.objects.get(id=spt_id)
    pimpinan = User.objects.filter(groups__name="pimpinan").first()
    pimpinan = pimpinan.profile
    selisih = (spt.tanggal_selesai - spt.tanggal_mulai).days
    context = {
        'spt': spt,
        'pimpinan': pimpinan,
        'selisih': selisih
    }
    return render(request, 'spt/laporan-spt.html', context)

def template_pdf(request, spt_id):
    spt = SPT.objects.get(id=spt_id)
    pimpinan = User.objects.filter(groups__name="pimpinan").first()
    pimpinan = pimpinan.profile
    
    return render(request, 'spt/pdf.html', {'spt': spt, 'pimpinan': pimpinan})

def spt_create(request):
    if request.method == "POST":
        
        data_post = request.POST.copy()
        data_post["nomor_spt"] = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        data_post["status"] = "diajukan"
        data_post["dibuat_oleh"] = request.user.id
        
        lampiran = request.FILES.getlist('lampiran')
        keterangan = request.POST.getlist('keterangan')
        
        # spt = SPT.objects.create(**data_post)
        
        form = SPTForm2(request.POST)
        formset = SPTLampiranFormSet(request.POST, request.FILES)
        
        # total = int(request.POST.get('lampiran-TOTAL_FORMS', 0))

        # for i in range(total):
        #     file = request.FILES.get(f'form-{i}-file')
        #     keterangan = request.POST.get(f'form-{i}-keterangan', '')
            
        #     print(keterangan, file)

            # if file:
            #     SPTLampiran.objects.create(
            #         spt=spt,
            #         file=file,
            #         keterangan=keterangan
            #     )
        
        # if form.is_valid() and formset.is_valid():
        #     spt = form.save(commit=False)
        #     spt.dibuat_oleh = request.user
        #     # spt.save()
            
        #     formset.instance = spt
        #     # formset.save()
            
        #     return redirect("spt_index")
    else:
        form = SPTForm2()
        formset = SPTLampiranFormSet()
        
    context = {
        "form": form,
        "formset": formset
    }
    return render(request, 'spt/create.html', context)

def spt_update(request, spt_id):
    spt = SPT.objects.get(id=spt_id)
    
    if request.method == "POST":
        form = SPTForm2(request.POST, instance=spt)
        formset = SPTLampiranFormSet(request.POST, request.FILES, instance=spt)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                spt = form.save(commit=False)
                
                # inject field backend
                spt.dibuat_oleh = request.user
                # optional:
                # spt.status = "updated"

                spt.save()
                formset.save()
                
                return redirect("spt_index")
    else:
        form = SPTForm2(instance=spt)
        formset = SPTLampiranFormSet(instance=spt)
        
    context = {
        "form": form,
        "formset": formset
    }
    return render(request, 'spt/update.html', context)
