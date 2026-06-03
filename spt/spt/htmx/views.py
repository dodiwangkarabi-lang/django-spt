from django.shortcuts import render
from django.http import HttpResponse

# services
from spt.spt.services import SPTServices

# forms
from spt.spt.web.forms import SPTForm

def spt_form_view(request):
    form = SPTForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        
        service = SPTServices.create
        
    return render(request, 'spt/htmx/create_spt.html')